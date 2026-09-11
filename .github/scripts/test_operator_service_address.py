#!/usr/bin/env python3
"""Render-only regression checks. Requires Helm 3 and PyYAML."""

import copy
import os
from pathlib import Path
import subprocess
import unittest

import yaml


CHART = Path(__file__).resolve().parents[2] / "helm" / "stunner"
HELM = os.environ.get("HELM", "helm")
OPTION = "stunnerGatewayOperator.deployment.useServiceAddress"
REPLICAS = "stunnerGatewayOperator.deployment.replicas"
OPERATOR = "stunner-gateway-operator-controller-manager"


def render(*settings, namespace="stunner-system", success=True):
    args = [HELM, "template", "test", str(CHART), "--namespace", namespace,
            "--include-crds", "--kube-version", "1.35.0"]
    for setting in settings:
        args.extend(["--set", setting])
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if not success:
        return result
    if result.returncode:
        raise AssertionError(result.stderr)
    return {(obj["kind"], obj["metadata"].get("namespace", ""),
             obj["metadata"]["name"]): obj
            for obj in yaml.safe_load_all(result.stdout) if obj}


def operator(objects, namespace="stunner-system"):
    return objects[("Deployment", namespace, OPERATOR)]


def address(deployment):
    manager = next(container for container in
                   deployment["spec"]["template"]["spec"]["containers"]
                   if container["name"] == "manager")
    return next(env for env in manager["env"]
                if env["name"] == "STUNNER_GATEWAY_OPERATOR_ADDRESS")


class ServiceAddressTests(unittest.TestCase):
    def test_default_and_explicit_opt_out_preserve_pod_address(self):
        default = render()
        self.assertEqual(default, render(f"{OPTION}=false"))
        deployment = operator(default)
        self.assertEqual(address(deployment), {
            "name": "STUNNER_GATEWAY_OPERATOR_ADDRESS",
            "valueFrom": {"fieldRef": {"apiVersion": "v1",
                                       "fieldPath": "status.podIP"}},
        })
        self.assertNotIn("strategy", deployment["spec"])

    def test_opt_in_changes_only_address_and_update_strategy(self):
        before, after = render(), render(f"{OPTION}=true")
        deployment = operator(after)
        self.assertEqual(deployment["spec"]["strategy"],
                         {"type": "Recreate", "rollingUpdate": None})
        self.assertEqual(address(deployment), {
            "name": "STUNNER_GATEWAY_OPERATOR_ADDRESS",
            "value": "stunner-config-discovery.stunner-system.svc",
        })
        service = after[("Service", "stunner-system", "stunner-config-discovery")]
        labels = deployment["spec"]["template"]["metadata"]["labels"]
        self.assertTrue(all(labels.get(k) == v for k, v in service["spec"]["selector"].items()))
        self.assertEqual(service["spec"]["ports"], [
            {"name": "cds", "port": 13478, "protocol": "TCP"}])
        normalized = copy.deepcopy(after)
        deployment = operator(normalized)
        del deployment["spec"]["strategy"]
        env = address(deployment)
        env.clear()
        env.update(address(operator(before)))
        self.assertEqual(before, normalized, "unrelated rendered objects changed")

    def test_service_address_follows_release_namespace(self):
        objects = render(f"{OPTION}=true", namespace="turn-control")
        self.assertEqual(address(operator(objects, "turn-control"))["value"],
                         "stunner-config-discovery.turn-control.svc")
        self.assertIn(("Service", "turn-control", "stunner-config-discovery"), objects)

    def test_service_address_follows_namespace_override(self):
        objects = render(f"{OPTION}=true", "namespace=turn-override")
        self.assertEqual(address(operator(objects, "turn-override"))["value"],
                         "stunner-config-discovery.turn-override.svc")
        self.assertIn(("Service", "turn-override", "stunner-config-discovery"), objects)

    def test_opt_in_rejects_zero_and_multiple_operators(self):
        for replicas in (0, 2):
            with self.subTest(replicas=replicas):
                result = render(f"{OPTION}=true", f"{REPLICAS}={replicas}", success=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("requires exactly one operator replica", result.stderr)
                self.assertFalse(result.stdout.strip())

    def test_opt_out_preserves_multiple_operators(self):
        deployment = operator(render(f"{OPTION}=false", f"{REPLICAS}=2"))
        self.assertEqual(deployment["spec"]["replicas"], 2)
        self.assertIn("valueFrom", address(deployment))
        self.assertNotIn("strategy", deployment["spec"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
