######################### eks data ###############################

data "local_file" "cluster_autoscaler_policy_file" {

  filename = "${path.module}/data/cluster_autoscaler_policy.json"
}

data "local_file" "eks_ingress_policy_file" {

  filename = "${path.module}/data/eks_ingress_policy.json"
}

data "local_file" "eks_assume_role_policy_file" {

  filename = "${path.module}/data/eks_assume_role_policy.json"
}

data "local_file" "eks_cluster_policy_file" {

  filename = "${path.module}/data/eks_cluster_policy.json"
}

data "local_file" "eks_nodegroup_assume_role_policy_file" {

  filename = "${path.module}/data/eks_nodegroup_assume_role_policy.json"
}

data "local_file" "aws_load_balancer_controller_policy_file" {

  filename = "${path.module}/data/aws_load_balancer_controller_policy.json"
}
