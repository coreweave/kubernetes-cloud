---
description: Delve deeper into VFX Cloud Studios on CoreWeave Cloud
---

# CoreWeave VFX Cloud Studio Reference Guide

The pages in this guide walk through everything you need to know in order to create a feature-rich VFX studio on CoreWeave Cloud while utilizing best practices and recommended solutions.&#x20;

{% hint style="info" %}
**Note**

These guides are intended as introductions to fundamental concepts, which can then further built upon. Where applicable, references to additional documentation have been provided in order to further explain configuration options and deployment methods.
{% endhint %}

## Recommended resources

Before diving in to the rest of this guide, reading the following resources is **strongly recommended.** These resources will help to familiarize you with the pieces and terminology that will be discussed later in this guide.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong></strong><span data-gb-custom-inline data-tag="emoji" data-code="2601">☁</span> <strong>Getting Started on CoreWeave Cloud</strong></td><td>An introduction to CoreWeave Cloud as a whole.</td><td></td><td><a href="../">..</a></td></tr><tr><td><strong></strong><span data-gb-custom-inline data-tag="emoji" data-code="26f5">⛵</span> <strong>Useful Kubernetes commands</strong></td><td>A cheat sheet of helpful, frequently-used Kubernetes commands.</td><td></td><td><a href="../../coreweave-kubernetes/useful-commands.md">useful-commands.md</a></td></tr><tr><td><strong></strong><span data-gb-custom-inline data-tag="emoji" data-code="1f5a5">🖥</span> <strong>Getting Started with Virtual Servers</strong></td><td>Learn about Virtual Servers on CoreWeave Cloud; what they are, what they're used for, and how to deploy and manage them.</td><td></td><td><a href="broken-reference">Broken link</a></td></tr></tbody></table>

## Getting Started with VFX Cloud studios

Like any VFX studio, CoreWeave Cloud studios are comprised of multiple parts, each of which is discussed in depth within this guide. The diagram below offers a visual example of how each part works together within the Cloud.

{% embed url="https://lucid.app/documents/embeddedchart/aba70634-17de-4a94-9721-a80f4eed5298" %}
A diagram showcasing how the components of a VFX studio fit together
{% endembed %}

## Authenticating using Active Directory

The examples contained within this guide assume a few things about the Cloud studio setup. For starters, it is assumed that authentication is desired, so for many of the examples throughout this guide, Active Directory is used for user management and authentication. As such, we have already [provisioned an Active Directory domain](../virtual-servers/examples/active-directory-environment-hosted-on-coreweave-cloud/provision-an-active-directory-domain-controller.md), which is required to use Active Directory for user authentication.

{% hint style="success" %}
**Tip**

Setting up an Active Directory domain may be a good place to start when setting up your Cloud studio, but you can also come back later to configure Active Directory after you have set up the other components.
{% endhint %}
