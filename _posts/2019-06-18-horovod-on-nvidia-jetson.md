---
id: 727
title: Horovod on NVIDIA Jetson
post_description:
  Horovod is a software framework for distributed training of neural networks. This is a short report on my setup for using a number of NVIDIA Jetson Developer Kits for distributed training with Tensorflow.

date: 2019-06-18T18:31:47+09:00
author: Peter Bryzgalov
layout: post
permalink: /horovod-on-nvidia-jetson/
categories:
  - Machine Learning
tags:
  - data parallelism
  - Horovod
  - Jetson AGX Xavier
  - Jetson TX2
  - Keras
  - machine learning
  - model training
  - Nvidia
  - NVIDIA Jetson
  - Tensorflow
---


<p class="has-medium-font-size">
Distributed training with Keras on NVIDIA Jetson TX2 and Xavier
</p>

Horovod (<a href="https://github.com/horovod/horovod" target="_blank" rel="noopener noreferrer">github</a>) is a software framework for distributed training of neural networks with Keras, Tensorflow, MxNet or PyTorch. Developed at Uber since 2017 it is still in beta version (latest release is v0.16.4 as of 2019/06/18).

This is a short report on my setup for using a number of NVIDIA Jetson Developer Kits for distributed training.

#### Prerequisites

Install on all machines: MPI, NCCL, Tensorflow, Keras, Horovod.

**MPI**
OpenMPI should have been already installed with the Jetpack. It is important to have the same version on all computers. Check with `$ mpirun --version`


**Horovod**

```bash
$ sudo apt-get install libffi6 libffi-dev
$ pip install --user horovod
```

### Run distributed training

If installation finished without errors, you are ready to run a test. I used <a rel="noopener noreferrer" href="https://github.com/horovod/horovod/blob/master/examples/keras_mnist.py" target="_blank">Keras MNIST example</a>.

It is important to have the script file on the PATH on all machines. If it&#8217;s not the case, you can use `-x` option to mpirun command to copy environment variable (PATH) to all machines.

To start training I used the following command:

```bash
$ mpirun -np 3 -H localhost:1,jetson1:1,jetson2:1 \
-mca btl_tcp_if_include eth0 -x NCCL_SOCKET_IFNAME=eth0 \
-bind-to none -map-by slot python keras_mnist.py
```

`-np 3` tells MPI that I need 3 processes: 3 machines each with 1 GPU: 3 processes in total.  
`-H localhost:1,jetson1:1,jetson2:1` use 1 GPU on localhost (Xavier in my case), 1 GPU on jetson1 and one on jetson2 host. You must be able to login to these hosts with SSH without password ( `~/.ssh/config` can help).  
`-mca btl_tcp_if_include eth0` and `-x NCCL_SOCKET_IFNAME=eth0` options for using eth0 network interface.  
`-bind-to none -map-by slot` OpenMPI options.


Below is the video of running Horovod Keras MNIST sample on the 3 machines.

**How fast is parallel training?** Check my notes below the video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/WPGue7c2PIU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Performance Analysis

After training the sample network in parallel, I trained it on Xavier and on TX2 with the same parameters without parallelisation. The only hyper-parameter changed is the learning rate, which is set in the sample code to be larger for parallel training: `lr = 1.0 * hvd.size()`. hvd.size() is the number of MPI processes, which in my case is 3 for parallel training and 1 for one-machine training. I ran training in parallel on 3 machines, on Xavier only and on TX2 only until validation accuracy reached <span style="color:red">0.99</span>.

The graph below shows time and validation accuracy per epoch for each training.

<img class="scalable" src="{{ '../wp-content/uploads/2019/06/training_logs-2.png' | relative_url }}" alt=""  />

Regarding epoch time (seconds per epoch) you can see, that:

  1. For parallel training one epoch time is about the same as epoch time on TX2 (the slowest type of machine).
  2. Epoch time on Xavier is the shortest &ndash; about 3 times shorter than on TX2.

### Conclusions

Though accuracy gain per epoch for parallel training is higher than for training on one machine, one parallel training epoch time is equal to epoch time on the slowest of machines. That is because parallel training is done in a synchronous manner and after each epoch all workers share model weight gradients. That means the process on Xavier finishes one epoch earlier, but have to wait for the other two processes on TX2-s to finish.

All-in-all, unbalance in performance between machines makes parallel training even slower than on one faster machine – Xavier. That, however, may change if more machines were used in training making accuracy gain per epoch even higher.

You can learn more about parallel training from this thorough post <a rel="noopener noreferrer" href="https://towardsdatascience.com/distributed-tensorflow-using-horovod-6d572f8790c4" target="_blank">Distributed TensorFlow using Horovod</a>.