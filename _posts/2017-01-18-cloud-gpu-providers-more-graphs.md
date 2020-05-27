---
id: 444
title: 'Cloud GPU  providers comparison &#8211; more graphs'
post_description:
  Interactive charts to compare cloud GPU providers by calculation time for a fixed amount of calculations.

date: 2017-01-18T11:30:14+09:00
author: Peter Bryzgalov
layout: post
# guid: http://comp.photo777.org/?p=444
permalink: /cloud-gpu-providers-more-graphs/
include_blocks:
  - cloud_gpus
  - cloud_gpus2
categories:
  - Cloud GPU providers
tags:
  - AMD
  - AWS
  - Cirrascale
  - cloud
  - cloud GPU
  - compare cloud GPUs
  - compare cloud providers
  - compare costs
  - compare price
  - comparison
  - cost
  - could providers
  - EC2
  - GPU
  - GPU performance
  - LeaderTelecom
  - Nvidia
  - Sakura internet
  - Softlayer
---

Continued from [the previous post](/cloud-gpu-providers-comparison/).

With the graphs below, you can compare calculation time and cost for a fixed amount of calculations in Floating Point Operations. (FLOPs<sup><a href="#notes">\*\*\*</a></sup>). Use the buttons above the charts to set calculations amount and the number of machines (virtual or bare metal; they are called nodes) used for calculations.


Important notice: we assume that a task can be run on multiple computers WITHOUT any slowdown. This means that on N machines the task will finish N times faster. This could be true, for instance, in the case of hyperparameters search when you have multiple independent tasks.

Graphs are not scaled when parameters change to make points movements clearly visible. To scale charts manually use “Autoscale” and “Reset axes” buttons that appear in the top right corner of the graphs when you bring the mouse cursor over it (on tablet devices tap the chart).

<p  class="note" id="updated">
  <p>
    <!--more-->
  </p>

  <div class="grouptitle">
    <h3>
      Filter offers in all graphs below using these charts
    </h3>

    <div style="float:none;">
    </div>

    <div id="dc_gpu_models">
      <title>
        Number of offers by GPU model
      </title>
    </div>

    <div class="dc_group">
      <div id="dc_gpus">
        <title>
          Number of GPUs
        </title>
      </div>

      <div id="dc_gpu_perf">
        <title>
          Total GPU performance (TFlops)
        </title>
      </div>
    </div>

    <div class="dc_group">
      <div id="dc_memory">
        <title>
          Memory (GB)
        </title>
      </div>

      <div id="dc_cpu_perf">
        <title>
          Total CPU performance (TFlops)
        </title>
      </div>
    </div>

    <div id="dc_providers">
      <title>
        Number of offers by Providers
      </title>
    </div>

    <div id="dc_end">
    </div>
  </div>

  <div id="messages">
  </div>

  <div class="grouptitle">
    <h3>
      Set calculation task complexity in EFLOPs and nodes number
    </h3>

    <div class="buttons">
      <h4>
        EFLOPs
      </h4>

      <div id="FLOPsScale" style="width: 100%;">
      </div>
    </div>

    <div class="buttons">
      <h4>
        nodes
      </h4>

      <div id="NodesScale" style="width: 100%;">
      </div>
    </div>

    <p>
      The graph below shows calculation time and cost necessary for calculating a task with task complexity set in <span title="Floating Point Operations * 10e18">EFLOPs</span><sup><a href="#notes">****</a></sup> on GPU(s) provided by each offer.
    </p>

    <div id="GPUtime_x_cost" style="width: 100%; height: 600px;">
    </div>

    <div id="offer_details1" class="note">
      &nbsp;
    </div>
  </div>

  <div class="grouptitle">
    <h3>
      Set calculation task complexity in EFLOPs and nodes number
    </h3>

    <div class="buttons">
      <h4>
        EFLOPs
      </h4>

      <div id="FLOPsScale_cpu" style="width: 100%;">
      </div>
    </div>

    <div class="buttons">
      <h4>
        nodes
      </h4>

      <div id="NodesScale_cpu" style="width: 100%;">
      </div>
    </div>

    <p>
      The graph below shows calculation time and cost necessary for calculating a task with the same complexity using only provided CPUs.
    </p>

    <div id="CPUtime_x_cost" style="width: 100%; height: 600px;">
    </div>

    <div id="offer_details2" class="note">
      &nbsp;
    </div>

    <!--div id="flops_4money" style="width: 100%; height: 600px;"></div-->

    <div class="note" id="notes">
      <p>
        * All sums are in USD. Offers based on other currencies are converted using today's rates from <a href="http://www.ecb.europa.eu/stats/exchange/eurofxref/html/index.en.html" target="_blank">European Central Bank</a>:
      </p>

      <div id="rates">
      </div>

      <p>
        All prices do not include taxes.
      </p>

      <p>
        ** Performance data shows single precision FLOPS for GPUs and single precision FLOPS for CPUs. <b>Beware that performance data is a rough estimate, and actual performance may vary greatly between applications.</b>
      </p>

      <p>
        *** Floating Point Operations (not to be confused with Flops &mdash; Floating Point Operations per Second).
      </p>


        **** EFLOPs = 1 * 10<sup>18</sup>FLOPs. TFLOPs = 1 * 10<sup>12</sup>FLOPs.
      </div>