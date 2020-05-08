---
id: 5
title: Docker network performance
date: 2014-06-16T14:54:50+09:00
author: Peter Bryzgalov
layout: post
permalink: /docker-network-performance/
categories:
  - Docker
tags:
  - communication
  - containers
  - Docker
  - network performance
  - networking
---
Here are some results of testing performance of different <a title="An open platform for developers and sysadmins" href="http://docker.com" target="_blank">Docker</a> Inter Container Communication (ICC) techniques.

Techniques I tested:

<table>
  <tr>
    <td>
      iptables
    </td>
    
    <td>
      Routing settings that give containers externally visible IP address as described here:  <a title="blog.codeaholics.org/2013/giving-dockerlxc-containers-a-routable-ip-address/" href="http://blog.codeaholics.org/2013/giving-dockerlxc-containers-a-routable-ip-address/" target="_blank">blog.codeaholics.org/2013/giving-dockerlxc-containers-a-routable-ip-address/</a>
    </td>
  </tr>
  
  <tr>
    <td>
      pipework
    </td>
    
    <td>
       <a title="github.com/jpetazzo/pipework" href="https://github.com/jpetazzo/pipework" target="_blank">github.com/jpetazzo/pipework</a>  – a tool for assigning external IP addresses to containers. It has two modes: using macvlan interface and using veth pairs. I used the second one – veth pairs.
    </td>
  </tr>
  
  <tr>
    <td>
       Docker link
    </td>
    
    <td>
      Docker feature for inter container communication (ICC). It doesn&#8217;t assign containers external IPs. <a title="docs.docker.com/userguide/dockerlinks/" href="https://docs.docker.com/userguide/dockerlinks/" target="_blank">docs.docker.com/userguide/dockerlinks/</a>
    </td>
  </tr>
  
  <tr>
    <td>
       Open vSwitch
    </td>
    
    <td>
      <a title="openvswitch.org" href="http://openvswitch.org" target="_blank">openvswitch.org</a><br /> Used version 2.1.0 with kernel support.
    </td>
  </tr>
</table>

Tested on Dell Poweredge D320 server with Xeon 1.8GHz, 4GB (1333MHz) RDIMM, 7200RPM SATA HDD  
OS Ubuntu server 12.04.4 LTS  
kernel 3.8.0-39  
Docker version 0.11.

Network performance was tested with iperf with the following client command:  
` iperf -c $ServerIP -P 1 -i 1 -p 5001 -f g -t 5`

Performance in Gbit/s, average for one container.

The following 3 setups was tested:

  1. One server container and multiple client containers with 1 iperf process in each container.
  2. Multiple servers and multiple clients. 1 iperf process in each container.
  3. One server container with one iperf server, multiple containers with multiple iperf clients in each container.

## One server and multiple clients

ICC performance between one container with one iperf server and multiple containers with one iperf client each. Average performance per container in Gbit/s.

<table style="color: #484848;">
  <tr>
    <th class="lastheader">
      client containers
    </th>
    
    <th class="lastheader">
      1
    </th>
    
    <th class="lastheader">
      2
    </th>
    
    <th class="lastheader">
      4
    </th>
    
    <th class="lastheader">
      8
    </th>
    
    <th class="lastheader">
      16
    </th>
    
    <th class="lastheader">
      20
    </th>
  </tr>
  
  <tr>
    <td>
      iptables
    </td>
    
    <td>
      10.0
    </td>
    
    <td>
      8.0
    </td>
    
    <td>
      4.2
    </td>
    
    <td>
      2.1
    </td>
    
    <td>
      1.0
    </td>
    
    <td>
      0.8
    </td>
  </tr>
  
  <tr>
    <td>
      pipework
    </td>
    
    <td>
      11.6
    </td>
    
    <td>
      8.3
    </td>
    
    <td>
      5.1
    </td>
    
    <td>
      2.7
    </td>
    
    <td>
      1.4
    </td>
    
    <td>
      1.0
    </td>
  </tr>
  
  <tr>
    <td>
      link
    </td>
    
    <td>
      12.0
    </td>
    
    <td>
      8.1
    </td>
    
    <td>
      4.9
    </td>
    
    <td>
      2.5
    </td>
    
    <td>
      1.2
    </td>
    
    <td>
      1.0
    </td>
  </tr>
  
  <tr>
    <td>
      ovs
    </td>
    
    <td>
      13.2
    </td>
    
    <td>
      11.0
    </td>
    
    <td>
      6.6
    </td>
    
    <td>
      3.3
    </td>
    
    <td>
      1.8
    </td>
    
    <td>
      1.4
    </td>
  </tr>
</table>



[<img class="wp-image-18 size-full" src="{{ '/wp-content/uploads/2014/06/ICC1-m-1.png' | relative_url }}" alt="1 server multiple clients"  />]({{ '/wp-content/uploads/2014/06/ICC1-m-1.png' | relative_url }})
_1 server &#8211; multiple clients_


## Multiple servers and multiple clients

ICC between multiple containers each with one iperf server inside, and multiple containers with one iperf client each. Client number _i_ connects to the server number _i (mod n)_, where _n_ is the number of servers.  
Below are the average performance results in Gbit/s.

<table style="color: #484848;">
  <tr>
    <th>
      servers
    </th>
    
    <th>
      1
    </th>
    
    <th>
      2
    </th>
    
    <th>
      4
    </th>
    
    <th>
      20
    </th>
  </tr>
  
  <tr>
    <th class="lastheader">
      clients
    </th>
    
    <th class="lastheader">
      1
    </th>
    
    <th class="lastheader">
      2
    </th>
    
    <th class="lastheader">
      4
    </th>
    
    <th class="lastheader">
      20
    </th>
  </tr>
  
  <tr>
    <td>
      iptables
    </td>
    
    <td>
      10.0
    </td>
    
    <td>
      8.3
    </td>
    
    <td>
      4.3
    </td>
    
    <td>
      0.8
    </td>
  </tr>
  
  <tr>
    <td>
      pipework
    </td>
    
    <td>
      11.6
    </td>
    
    <td>
      10.0
    </td>
    
    <td>
      5.5
    </td>
    
    <td>
      1.3
    </td>
  </tr>
  
  <tr>
    <td>
      link
    </td>
    
    <td>
      12.0
    </td>
    
    <td>
      9.1
    </td>
    
    <td>
      5.1
    </td>
    
    <td>
      1.1
    </td>
  </tr>
  
  <tr>
    <td>
      ovs
    </td>
    
    <td>
      13.2
    </td>
    
    <td>
      10.8
    </td>
    
    <td>
      5.6
    </td>
    
    <td>
      1.4
    </td>
  </tr>
</table>

[<img class="wp-image-19 size-full" src="{{ '/wp-content/uploads/2014/06/ICCn-m-1.png' | relative_url }}" alt="ICCn-m-1"  />]({{ '/wp-content/uploads/2014/06/ICCn-m-1.png' | relative_url }})
_Multiple servers and multiple clients with 1 iperf process inside._

&nbsp;

## One server and multiple containers with multiple iperf clients inside

Average performance per container in Gbit/sec.  
Number of containers x number of iperf clients in one container

<table>
  <tr>
    <th class="lastheader">
    </th>
    
    <th class="lastheader">
      1 x 1
    </th>
    
    <th class="lastheader">
      1 x 2
    </th>
    
    <th class="lastheader">
      1 x 4
    </th>
    
    <th class="lastheader">
      1 x 16
    </th>
    
    <th class="lastheader">
      2 x 1
    </th>
    
    <th class="lastheader">
      4 x 1
    </th>
    
    <th class="lastheader">
      16 x 1
    </th>
    
    <th class="lastheader">
      2 x 2
    </th>
    
    <th class="lastheader">
      4 x 4
    </th>
    
    <th class="lastheader">
      16 x 16
    </th>
  </tr>
  
  <tr>
    <td>
      pipework
    </td>
    
    <td>
      11.16
    </td>
    
    <td>
      9.81
    </td>
    
    <td>
      3.38
    </td>
    
    <td>
      1.07
    </td>
    
    <td>
      9.33
    </td>
    
    <td>
      4.99
    </td>
    
    <td>
      1.52
    </td>
    
    <td>
      4.63
    </td>
    
    <td>
      1.20
    </td>
    
    <td>
      0.04
    </td>
  </tr>
  
  <tr>
    <td>
      link
    </td>
    
    <td>
      12.10
    </td>
    
    <td>
      7.70
    </td>
    
    <td>
      3.30
    </td>
    
    <td>
      0.80
    </td>
    
    <td>
      8.20
    </td>
    
    <td>
      4.90
    </td>
    
    <td>
      1.20
    </td>
    
    <td>
      4.30
    </td>
    
    <td>
      1.10
    </td>
    
    <td>
      0.00
    </td>
  </tr>
  
  <tr>
    <td>
      ovs
    </td>
    
    <td>
      13.06
    </td>
    
    <td>
      11.14
    </td>
    
    <td>
      6.36
    </td>
    
    <td>
      1.54
    </td>
    
    <td>
      11.24
    </td>
    
    <td>
      6.63
    </td>
    
    <td>
      1.99
    </td>
    
    <td>
      6.40
    </td>
    
    <td>
      1.50
    </td>
    
    <td>
      0.06
    </td>
  </tr>
</table>

[<img class="alignnone size-full wp-image-45" src="{{ '/wp-content/uploads/2014/06/ICC1-n-m.png' | relative_url }}" alt="ICC1-n-m"  />]({{ '/wp-content/uploads/2014/06/ICC1-n-m.png' | relative_url }})

### Conclusion

Running iperf clients in different containers gives better performance compared with the same number of clients running in one container (compare 1&#215;4 and 4&#215;1).