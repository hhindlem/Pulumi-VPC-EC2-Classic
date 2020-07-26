# Pulumi-VPC-EC2-Classic

# An example Pulumi AWS EC2 VPC for EC2-Classic accounts

## Background
If you try to run the Pulumi tutorial example [aws-py-webserver](https://www.pulumi.com/docs/tutorials/aws/ec2-webserver/), which points to the code [Pulumi example aws-py-webserver](https://github.com/pulumi/examples/blob/master/aws-py-webserver), and if you get the error:
> error: Error launching source instance: VPCResourceNotSpecified: The specified instance type can only be used in a VPC. A subnet ID or network interface ID is required to carry out the request.

you probably have an early (pre 2014) EC2-Classic AWS account. You can confirm this by looking in the upper right corner of your [EC2 console home page](https://console.aws.amazon.com/ec2/v2/home). 
>Account attributes
>Supported platforms
>
> - EC2
> - VPC

You can read more about EC2-Classic here: [AWS Userguide page about EC2-Classic accounts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html).  And there's more about modern AWS VPC accounts here: [aws-vpc-explained](https://www.infoq.com/articles/aws-vpc-explained/).

## A Solution

One solution is to build the VPC plumbing in Pulumi. See my file '\_\_main\_\_.py'.  (I'm not an expert with AWS VPCs, and I'm just a beginner with Pulumi, so there are probably aspects of this that I still don't have correct.)

## Running the example

Since I've written the example to enable ssh into the new instance, it assumes that you've already generated a key-pair named 'test':
```sh
$ ssh-keygen -q -t rsa -f test -m PEM -N ""
```

After doing "pulumi up", you should be able to:
```sh
$ curl $(pulumi stack output publicHostName)
Hello, World!!
```

and:
```sh
$ ssh  -i test ec2-user@$(pulumi stack output publicIp)
```

## Other Solutions

Another solution seems to be to convert your account. [Here](https://github.com/hashicorp/terraform/issues/4367) are some Terraform folks discussing the issue, and [one of the posts](https://github.com/hashicorp/terraform/issues/4367#issuecomment-513480968) suggests: aws-console -> new support issue -> "Regarding: Account and Billing Support" -> "Service: Account" -> "Category: Convert EC2 Classic to VPC".  I haven't yet tried this.

There is also a chance that Pulumi [Crosswalk's](https://www.pulumi.com/docs/guides/crosswalk/aws/) [Crosswalk VPC](https://www.pulumi.com/docs/guides/crosswalk/aws/vpc/) library will solve the problem, but (as of July, 2020) it's [not yet available](https://github.com/pulumi/pulumi-awsx/issues/308) for python.

Also maybe of interest is jen20's [AWS VPC Component for Pulumi](https://github.com/jen20/pulumi-aws-vpc), which seems roughly analogous to the goals of Pulumi's Crosswalk.  I get "Error creating EIP: AddressLimitExceeded: Too many addresses allocated", but I haven't tracked down the problem.  I'm assuming it's something to do with my AWS account being EC2-Classic.

# License
MIT
