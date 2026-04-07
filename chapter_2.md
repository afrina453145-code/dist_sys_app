COURSE: DISTRIBUTED SYSTEMS
CHAPTER 2: COMMUNICATION

This is a complete, high-density slide set covering the full syllabus. Each section is broken down into 2-3 slides focusing on mechanical definitions and structural clarity.

---

## **1. Foundations & Motivation**

### **Slide 1.1: Why Structure?**
* **The Complexity Problem:** Modern networking involves billions of heterogeneous devices; managing them requires a structured "stack" to ensure interoperability between different hardware and software.
* **Protocol Definition:** A formal set of rules for communication.
    * **Syntax:** Data format and coding.
    * **Semantics:** Meaning of each bit pattern/control information.
    * **Timing:** Speed matching and sequencing of messages.
* **History:** Developed from **ARPANET** (1960s) to the modern Internet, evolving from research experiments to a global utility via standardized protocol suites.

### **Slide 1.2: The Layering Principle**
* **Engineering Principle:** Breaking a system into independent levels. 
* **Separation of Concerns:** Each layer handles one specific task (e.g., routing, bit transmission).
* **Abstraction:** Each layer provides a **Service** to the layer above while hiding its internal implementation.
* **Service Primitives:** The specific operations (LISTEN, CONNECT, SEND) used to interface between layers.
* **Standardization Bodies:** **ISO** (Theory), **IETF** (Internet Standards/RFCs), **IEEE** (Physical/Hardware standards like 802.11).

### **Slide 1.3: Communication Logic**
* **Encapsulation:** The core mechanism. A layer takes data from the one above and adds its own **Header** (and sometimes Trailer).
* **Protocol Stack:** The specific set of protocols used by a system to enable communication.
* **Peer-to-Peer Communication:** * **Logical:** Layer $N$ on Host A "talks" directly to Layer $N$ on Host B.
    * **Physical:** Data actually moves down the stack, across the wire, and up the destination stack.
* **Trade-offs:** Modularity makes systems easier to build/fix, but adds **Performance Overhead** due to multiple headers and processing at each layer.

---

## **2. OSI & 3. TCP/IP Models**

### **Slide 2.1: The OSI Reference Model**
* **Purpose:** A 7-layer universal reference model designed for vendor interoperability.
* **Layer 7 (Application):** User-facing services.
* **Layer 6 (Presentation):** Data formatting and encryption.
* **Layer 5 (Session):** Managing dialogs and checkpoints.
* **Layer 4 (Transport):** End-to-end reliability.
* **Layer 3 (Network):** Path finding (Routing).
* **Layer 2 (Data Link):** Node-to-node hop.
* **Layer 1 (Physical):** Raw bit transmission.

### **Slide 2.2: TCP/IP Model (The Practical Winner)**
* **Origins:** DARPA/ARPANET. Won because it was implemented and proven before OSI was finalized.
* **Structure:** 4 Layers.
    1.  **Application:** Combines OSI 5, 6, 7.
    2.  **Transport:** Handles process-to-process communication.
    3.  **Internet:** Handles host-to-host routing.
    4.  **Network Access:** Handles physical hardware/links.
* **RFC (Request for Comments):** The official documents defining TCP/IP standards.

### **Slide 2.3: PDUs and Mapping**
* **PDU (Protocol Data Unit):** The name for data at each layer.
    * **Data:** Application Layer.
    * **Segment:** Transport Layer.
    * **Packet:** Network/Internet Layer.
    * **Frame:** Data Link Layer.
    * **Bits:** Physical Layer.
* **Comparison:** OSI is "Top-Down" (Theoretical), TCP/IP is "Bottom-Up" (Implementation-led).

---

## **4. Encapsulation & 5. Physical Concepts**

### **Slide 4.1: Encapsulation Mechanics**
* **Down the Stack:** Data $\rightarrow$ Add TCP Header (Segment) $\rightarrow$ Add IP Header (Packet) $\rightarrow$ Add Ethernet Header/Trailer (Frame).
* **Up the Stack:** Each layer reads and "strips" its specific header, passing the payload up (**Decapsulation**).
* **Multiplexing Identifiers:** How layers direct data.
    * **L2:** MAC Address.
    * **L3:** IP Address.
    * **L4:** Port Number.
* **MTU (Maximum Transmission Unit):** The largest frame size a link can carry; if a packet exceeds this, **Fragmentation** occurs.

### **Slide 5.1: Signal Transmission**
* **Analog vs. Digital:** Continuous waves vs. discrete pulses.
* **Modulation:** Altering a carrier wave (AM, FM, QAM) to represent digital data.
* **Nyquist Theorem:** Max data rate for a noiseless channel ($2B \log_2 L$).
* **Shannon’s Theorem:** Max data rate for a noisy channel ($B \log_2 (1 + S/N)$).
* **Mediums:** Twisted pair (cheap), Fiber optic (high bandwidth/distance), Wireless (radio/infrared).

### **Slide 5.2: Performance Metrics**
* **Bandwidth:** Theoretical capacity of the medium.
* **Throughput:** Actual data transferred per unit time.
* **Goodput:** Useful data delivered (excludes headers and retransmissions).
* **Latency:** Delay composed of **Propagation**, **Transmission**, **Processing**, and **Queuing** time.
* **Jitter:** Variation in latency; critical for real-time traffic like VoIP.

---

## **6. Transport Layer Deep Dive**

### **Slide 6.1: TCP (Transmission Control Protocol)**
* **Characteristics:** Connection-oriented, reliable, ordered, byte-stream.
* **3-Way Handshake:** **SYN** $\rightarrow$ **SYN-ACK** $\rightarrow$ **ACK** to establish state.
* **4-Way Teardown:** **FIN** $\rightarrow$ **ACK** $\rightarrow$ **FIN** $\rightarrow$ **ACK** to close.
* **Reliability:** Uses **Sequence Numbers** and **Cumulative ACKs**. 
* **Retransmission:** Triggered by Timeouts or "Fast Retransmit" (3 duplicate ACKs).
* **TIME_WAIT:** A state ensuring late packets don't interfere with new connections.

### **Slide 6.2: TCP Congestion & Flow Control**
* **Flow Control:** **Sliding Window** mechanism; the receiver tells the sender how much data it can buffer.
* **Congestion Control:** Prevents network collapse.
    * **Slow Start:** Double transmission rate every RTT.
    * **AIMD:** Additive Increase (linear), Multiplicative Decrease (cut in half on loss).
* **Nagle’s Algorithm:** Buffers small bits of data to send one large packet (reduces overhead).

### **Slide 6.3: UDP & Comparisons**
* **UDP (User Datagram Protocol):** Connectionless, unreliable, message-oriented. 
* **Header:** Minimal (8 bytes). Only Port numbers, Length, and Checksum.
* **Use Cases:** DNS, DHCP, Streaming, Gaming (where speed > reliability).
* **Comparison:** * **TCP:** Heavy, slow, guaranteed.
    * **UDP:** Light, fast, best-effort.

---

## **7. IP Addressing & Routing Deep Dive**

### **Slide 7.1: IPv4 & Subnetting**
* **IPv4 Structure:** 32-bit address, dotted-decimal notation.
* **Subnet Mask:** Defines the boundary between Network ID and Host ID.
* **CIDR (Classless Inter-Domain Routing):** Flexible notation (e.g., `/24`).
* **Special IPs:** `127.0.0.1` (Loopback), `255.255.255.255` (Broadcast), **RFC 1918** (Private IPs).
* **NAT (Network Address Translation):** Maps private local IPs to one public IP to save address space.

### **Slide 7.2: IPv6 & Modern Addressing**
* **IPv6 Structure:** 128-bit address, hexadecimal notation.
* **Key Differences:** No broadcast (uses multicast), no fragmentation by routers, simplified header.
* **SLAAC:** Allows devices to auto-configure their own IP without DHCP.
* **Dual Stack:** Running IPv4 and IPv6 simultaneously during transition.

### **Slide 7.3: Routing Algorithms & Protocols**
* **Routing Table:** Map used by routers to decide the next hop based on **Longest Prefix Matching**.
* **Distance Vector (RIP):** Based on hop count; suffers from "Count-to-Infinity" problem.
* **Link State (OSPF):** Each router builds a full map of the network (Dijkstra’s algorithm).
* **BGP (Border Gateway Protocol):** The "glue" of the Internet; routes between **Autonomous Systems (AS)** using Path Vectors.

---

## **8. Error Detection & Correction**

### **Slide 8.1: Detection Mechanisms**
* **Checksum:** Summing data bits; used in IP/TCP headers. Simple but weak against some burst errors.
* **Parity Bits:** Single bit added to ensure total 1s are even or odd.
* **CRC (Cyclic Redundancy Check):** Polynomial division. Highly effective at detecting burst errors; standard for Ethernet/Disks.

### **Slide 8.2: Correction & ARQ**
* **Hamming Codes:** Uses extra parity bits to identify and fix single-bit errors via **Hamming Distance**.
* **FEC (Forward Error Correction):** Sending enough redundant data so the receiver can fix errors without retransmitting.
* **ARQ (Automatic Repeat Request):**
    * **Stop-and-Wait:** Send 1, wait for ACK.
    * **Go-Back-N:** Send $N$, if one fails, resend all from that point.
    * **Selective Repeat:** Only resend the specific missing packet.

---

## **9. Data Formatting & Serialization**

### **Slide 9.1: The Serialization Problem**
* **Definition:** Converting in-memory objects into a byte stream for transmission.
* **Endianness:** **Big Endian** (Network Byte Order) vs. **Little Endian** (Host Order). Functions `htonl()`/`ntohl()` convert between them.
* **Marshalling:** Packaging data and arguments for a Remote Procedure Call (RPC).

### **Slide 9.2: Formats & Standards**
* **Text-based:** **JSON**, **XML**. Human-readable, flexible, but slow and bulky.
* **Binary:** **Protobuf**, **Avro**, **Thrift**. Compact, fast, requires a schema.
* **IDL (Interface Definition Language):** A language-neutral way to define data structures (e.g., `.proto` files).
* **Schema Evolution:** The ability to change data structures without breaking old clients (Backward/Forward compatibility).

---

## **10. Application Layer Protocols**

### **Slide 10.1: HTTP & DNS**
* **HTTP/1.1:** Persistent connections, but has **Head-of-Line Blocking**.
* **HTTP/2:** Multiplexing many requests over one TCP connection.
* **HTTP/3:** Uses **QUIC (UDP)** to eliminate TCP-level blocking and speed up handshakes.
* **DNS:** A hierarchical, distributed database for name resolution (Recursive vs. Iterative queries).

### **Slide 10.2: RPC & Messaging**
* **RPC (Remote Procedure Call):** Executes a function on a remote server as if it were local.
* **gRPC:** Modern RPC using HTTP/2 and Protobuf.
* **Messaging Protocols:**
    * **MQTT:** Lightweight Pub/Sub for IoT.
    * **AMQP/Kafka:** High-throughput queuing for distributed backends.
* **WebSockets:** Full-duplex, persistent connection initiated via an HTTP "Upgrade" handshake.

---

## **11. Socket Programming**

### **Slide 11.1: The Socket API**
* **Socket Abstraction:** An endpoint for communication (IP + Port).
* **Lifecycle:**
    * **Server:** `socket()` $\rightarrow$ `bind()` $\rightarrow$ `listen()` $\rightarrow$ `accept()`.
    * **Client:** `socket()` $\rightarrow$ `connect()`.
* **Types:** `SOCK_STREAM` (TCP) vs. `SOCK_DGRAM` (UDP).

### **Slide 11.2: Advanced I/O**
* **Blocking vs. Non-blocking:** Whether the program waits for data or continues execution.
* **I/O Multiplexing:** `select`, `poll`, `epoll`. Allows one thread to monitor thousands of sockets for activity.
* **Socket Buffers:** Kernel-level memory for sending and receiving data; overflows lead to packet loss.

---

## **12. Security Across Layers**

### **Slide 12.1: SSL/TLS & IPSec**
* **TLS (Transport Layer Security):** Sits between Transport and Application. Uses a **Handshake** for key exchange and certificates for identity.
* **IPSec:** Security at the Network layer; provides encryption for all traffic between two points (VPNs).
* **Chain of Trust:** Certificates are signed by **Certificate Authorities (CAs)** to prove ownership.

### **Slide 12.2: Layered Attacks**
* **L2:** ARP Spoofing (redirecting local traffic).
* **L3/L4:** IP Spoofing, DDoS (SYN flooding).
* **L7:** DNS Poisoning, SQL Injection, Man-in-the-Middle (MitM).
* **Defense:** Firewalls (Packet filtering), VPNs (Tunneling), and Encryption.

---

## **13. Performance & 14. Real-World Connections**

### **Slide 13.1: Optimization Techniques**
* **Bandwidth-Delay Product:** The "volume" of the network pipe ($B \times D$).
* **Bufferbloat:** Excessive buffering causing high latency.
* **Zero-Copy:** Technique where the CPU does not copy data between kernel and user space, increasing speed.
* **CDN:** Moving content to the "Edge" to reduce propagation delay.

### **Slide 14.1: Distributed Systems Integration**
* **Service Mesh (Istio):** A dedicated infrastructure layer for service-to-service communication, handling retries and security.
* **Overlay Networks:** Logical networks built on top of others (e.g., P2P like BitTorrent).
* **Heartbeats/Gossip:** Protocols used to detect failures and spread state across a cluster.
* **CAP Theorem:** Network partitions (failures at L3) force a choice between Consistency and Availability.