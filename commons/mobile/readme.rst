Mobility Traffic Profiles for OPNFV
===================================

Mobility User-Plane
+++++++++++++++++++

The following tables describe per-session average (in a range) for user-plane traffic related to classes of applications.

Downlink Mobility User-Plane
----------------------------

.. list-table:: Downlink Mobility User-Plane
   :widths: 25 25 25 25
   :header-rows: 1

   * - Service/protocol
     - Downlink Packet Size (bytes)
     - Downlink Flow Size (KB)
     - Downlink per-flow Throughput (Kbps)

   * - Browsing + Apps
     - 1,220 - 1,260
     - 40 - 55
     - 130 - 253

   * - HTTPS traffic
     - 1,050 - 1,085
     - 32 - 40
     - 107 - 124

   * - Video Streaming
     - 1,360 - 1,390
     - 545 - 650
     - 690 - 790

   * - VoLTE bearer (media, excluding signaling)
     - 84 – 102
     - 116 - 142
     - 18 - 24


Uplink Mobility User-Plane
--------------------------
.. list-table:: Uplink Mobility User-Plane
   :widths: 25 25 25 25
   :header-rows: 1

   * - Service/protocol
     - Uplink Packet Size (bytes)
     - Uplink Flow Size (KB)
     - Uplink per-flow Throughput (Kbps)

   * - Browsing + Apps
     - 90 – 120
     - 3 – 10
     - 6 – 18

   * - HTTPS traffic
     - 140 – 200
     - 5 – 12
     - 8 – 15

   * - Video Streaming
     - 50 – 110
     - 10 – 20
     - 12 - 20

   * - VoLTE bearer (media, excluding signaling)
     - 84 – 102
     - 112 - 135
     - 18 - 24


Mobility User-Plane Traffic Distribution
----------------------------------------
.. list-table:: Mobility User-Plane Traffic Distribution
   :widths: 33 33 33
   :header-rows: 1

   * - Service/protocol
     - Downlink
     - Uplink

   * - HTTP
     - 40 - 70% (60 – 40 split between ‘browsing + apps’ and ‘streaming’)
     - 30 - 50% (55 – 45 split between ‘browsing + apps’ and ‘streaming’)

   * - HTTPS
     - 25 - 50%
     - 40 - 60%

   * - Email
     - 1%
     - 3%

   * - P2P
     - 0.1%
     - 0.5%

   * - VoLTE
     - 0-5%
     - 5-30%

   * - Others
     - 4%
     - 8%

Mobility Control-Plane
++++++++++++++++++++++

This section will provide average per-session mobility control-plane traffic for various protocols associated with applications.

Mobility Sessions per Hour
++++++++++++++++++++++++++

This section will provide per-hour average and min-max ranges for mobility application sessions.
