---
description: Deploy applications onto CoreWeave Cloud with just a few button clicks
---

# Applications Catalog

The [CoreWeave Cloud applications Catalog](https://apps.coreweave.com) offers many useful applications that can be deployed and ready to use in just a few clicks. Throughout CoreWeave's documentation, particularly in examples, there will be instructions to deploy an application from the Catalog. Here is a basic overview of how the Catalog works, and how to deploy applications from within it.

<figure><img src="../../.gitbook/assets/image (24).png" alt="Screenshot: The Catalog home page"><figcaption><p>The Catalog home page</p></figcaption></figure>

## Access the Catalog

To access the Catalog, first log in to your CoreWeave Cloud account, then navigate to the **Applications** page on the left-hand menu.

<figure><img src="../../.gitbook/assets/image (10) (2).png" alt=""><figcaption></figcaption></figure>

## Find applications

The **Applications** tab at the top will display all applications you've deployed into your namespace. To get to the Catalog, click the **Catalog** tab.

From here, you can either search for an application by directly entering its name in the search bar, or you can filter by application type by clicking the filter boxes on the left-hand side.

<figure><img src="../../.gitbook/assets/image (19) (3).png" alt="Screenshot: The filter boxes can be used to search by application type, or a specific application may be searched for using the search bar"><figcaption><p>The filter boxes can be used to search by application type, or a specific application may be searched for using the search bar</p></figcaption></figure>

## Deploy applications

### About page

<figure><img src="../../.gitbook/assets/image (21).png" alt="Screenshot of application preview page"><figcaption><p>Application package information will be displayed on the left-hand side</p></figcaption></figure>

After clicking on the application you'd like to deploy, you'll be brought to the application's **about page**, where you can learn all about the application. From this page, you can also select the application's **Package Version** from the upper right-hand corner of the screen. Additional summary information will be included on the left-hand side of the screen.

Finally, when you're ready to deploy the application, you can click on the **Deploy** button from either the top right-hand corner or the bottom right-hand corner of the page.

### Deployment page

<figure><img src="../../.gitbook/assets/image (12).png" alt=""><figcaption><p>An application's deployment page</p></figcaption></figure>

Different applications will provide different configuration options on the **deployment page**. Typically, you can select to which data center region an application will be deployed, as well as some other basic configuration settings like resource limits. Some applications will also expose application-specific settings to you on this page.

### YAML tab

<figure><img src="../../.gitbook/assets/image (20).png" alt=""><figcaption><p>An application's deployment YAML</p></figcaption></figure>

If you would like a greater degree of control over the configuration of the application, or you'd like to save the configurations to deploy more applications, another way to configure applications is by clicking the **YAML** tab at the top of the page.

This YAML configuration exposes additional configuration options, and allows you to edit and save the YAML manifest to your specifications. It is not required to engage with the application's YAML - configuring an application from the **Form** tab is just fine.

### Changes tab

<figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption><p>An application's changes tab</p></figcaption></figure>

The **Changes** tab is a useful comparison tool that displays what configurations have been altered that are now different to the package defaults.
