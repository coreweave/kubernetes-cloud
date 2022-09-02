---
description: CoreWeave Requirements and Pricing for BYOIP
---

# Bring Your Own IP

**Last modified:  March 15, 2022**

These Requirements for BYOIP are incorporated in CoreWeave’s Terms of Service (TOS). By requesting BYOIP from CoreWeave, you agree to be bound by these Requirements and you acknowledge and agree to all of CoreWeave’s reservations of rights.

CoreWeave AS Number: **33425**&#x20;

_CoreWeave only supports IPv4 addressing at this time_

* Each subnet you request CoreWeave to advertise must not currently be in the global internet routing table, must be solely owned and controlled by the Customer, and must be portable space.&#x20;
* Customers must supply and maintain with CoreWeave a valid abuse email contact for any abuse related mail.
* The addresses in the IP address range supplied to CoreWeave must have a clean history. CoreWeave may investigate the reputation of the IP address range and reserves the right to reject or remove any IP address range from service if it contains an IP address that has a poor reputation or is associated with malicious behavior.
* The minimum supported subnet size is a /24 block.
* The block(s) must have a route object in one of the mainstream route object registries such as ARIN, RIPE, RADB.&#x20;
  * This route object will also need to list CoreWeave’s AS Number (33425) as an origin.&#x20;
  * If you do not have a routing registry that you can update, CoreWeave can register the object(s) for you, at your request.
* If the block has been RPKI signed, then as with the route object, CoreWeave’s AS must be added to a new [ROA request](https://www.arin.net/resources/manage/rpki/faq/#what-is-a-roa).
* Prior to advertising routes for your prefix, you must submit to CoreWeave a written Letter of Authorization (LOA) on the Customer’s entity letterhead that contains the entity’s full legal name and principal address and phone number, authorizing CoreWeave to announce the Customer owned IP space on Customer’s behalf. The LOA must be signed by an authorized representative of the Customer entity. The LOA should state the following: “We \[Customer] at AS\[ASN] authorize CoreWeave at AS33425 to announce our IP block \[x.x.x.x/yy] for an indefinite period of time,” and include the date and the name and title of the person signing the LOA. The LOA is a legally binding document and must contain a wet signature. It must be in .pdf format. LOAs in jpeg or png will not be accepted.

**Example Route Object:**

```
route:  	216.153.48.0/20
origin: 	AS33425
descr:  	CoreWeave, Inc.
admin-c:	SALAN13-ARIN
tech-c: 	BJB20-ARIN
remarks:	https://coreweave.com
notify: 	noc@coreweave.com
mnt-by: 	MAINT-AS33425
changed:	bbianchi@coreweave.com 20211021  #21:29:43Z
source: 	RADB
```

**Pricing**

One-time nonrefundable setup fee of $4.00 per IPv4 address, payable upon CoreWeave’s acceptance of Customer’s LOA.

**Reservation of Rights**

* CoreWeave is not responsible for, and does not provide, any DDoS protections for your blocks. If your block is the victim of a cyberattack, CoreWeave expressly reserves any and all rights to take whatever measures are necessary, in its sole discretion, to protect the security, integrity and availability of the CoreWeave platform, including but not limited to, at any time, withdrawing the announcement of your block(s). CoreWeave will notify the abuse contact on file.
* If a Customer’s advertised block is suspected, in CoreWeave’s sole discretion, or found to be in use for malicious or harmful purposes, CoreWeave expressly reserves the right to withdraw all of the Customer’s route advertisement. CoreWeave will notify the abuse contact on file.
* Continued participation in this configuration constitutes your acceptance of the TOS, the CoreWeave Acceptable Use Policy and any other applicable policies.

These CoreWeave Requirements for BYOIP are subject to change, in CoreWeave’s sole discretion.  Please check back regularly to ensure you are satisfying all of the requirements.  Failure to meet any requirement may result in the immediate suspension of your BYOIP subnet advertisements.&#x20;
