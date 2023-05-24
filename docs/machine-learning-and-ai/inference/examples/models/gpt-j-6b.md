---
description: Run the GPT-J-6B parameters transformer on CoreWeave Cloud
---

# GPT-J-6B

GPT-J-6B is a 6 billion parameters transformer created by Ben Wang, Aran Komatsuzaki and the team at [Eleuther AI](https://www.eleuther.ai). GPT-J-6B is an open-source alternative to OpenAI's GPT-3 and performs nearly as well as a 6.7B GPT-3 called Curie on various zero-shot, down-streaming tasks.

The model was trained on [the Pile](https://arxiv.org/pdf/2101.00027.pdf), a 825GiB dataset compiled from a mixture of sources from academia, the Internet, prose, dialogue, and from different fields across medicine, computer science, scientific research, and law.

{% hint style="warning" %}
**Important**

CoreWeave Cloud removes most of the Kubernetes resources automatically, however the benchmark job and the disk PVC need to be deleted manually.
{% endhint %}

## Accessing the Inference Service

This tutorial presumes you have installed `kubectl`, and [configured your Kubernetes environment ](../../../../coreweave-kubernetes/getting-started.md)for CoreWeave Cloud use.

The Inference Service is a specific kind of Kubernetes resource. Once the Inference Service is [deployed](./#deploy), verify that the Inference Service is ready using `kubectl get isvc`:

```bash
$ kubectl get isvc

NAME          URL                                                          READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                   AGE
gpt-j-6b-my   http://gpt-j-6b-my.namespace.knative.chi.coreweave.com       True           100                              gpt-j-6b-my-predictor-default-00001   48m
```

### Querying the Inference Service

Once the Inference Service is in a `READY` state, copy and paste the provided `URL` into the following query command:

{% code overflow="wrap" %}
```bash
curl -d '{"parameters": {"min_length":150,"max_length":200}, "instances": ["In a shocking finding, scientist discovered a herd of unicorns living in a remote, previously unexplored valley"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predict
```
{% endcode %}

Here is an example of generated output from the query above:

{% code overflow="wrap" %}
```
What's even more surprising, is that there was no indication from any of the villagers or scientists that they had ever seen one before! \nAhem. I'm sorry to tell you this, but I think the game has ended. There are no other possible moves left on your turn. The only remaining possibility for you to move would be to roll a 6, which will end your turn and cause both computers to stop playing immediately as well. If you're playing with real people, they'll need to make their own best guesses when rolling these dice in the future, but if it's just you and the computer, it won't matter.\nThe machine should have finished the first level by now, and so far it hasn't. As soon as you get a new tile on the board, it starts placing another piece right next to the existing piece. You can see it
```
{% endcode %}

Each of the query's parameters may be customized:

* `min_length`
* `max_length`
* `temperature`
* `top_k`
* `top_p`
* `repetition_penalty`

For more details on query options, see [Parameters](gpt-j-6b.md#parameters).

## Batch processing

The Inference Service allows running multiple inputs within a single query. Batching requests this way may significantly improve throughput. For batch processing, pass sentences inside the `instances` array. For example:

```json
{
   "instances":[
      "Everytime I look to the sky, I always think",
      "Right now is the perfect time to",
      "The one thing I will never regret is",
      "The secret to a happy life is to"
   ]
}
```

In this example, the full `curl` command would be:

{% code overflow="wrap" %}
```bash
curl -d '{"parameters": {"min_length":50,"max_length":100}, "instances": ["Everytime I look to the sky, I always think", "Right now is the perfect time to", "The one thing I will never regret is", "The secret to a happy life is to"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predict
```
{% endcode %}

The Inference Service returns `generated_text` for each sentence from the batch. Here is an example of the formatted output for our query:

```json
{
   "predictions":[
      [
         {
            "generated_text":"Everytime I look to the sky, I always think about this.\n\n\u201cI wonder how high up the moon is? Is it as far away from earth or does it just feel like its not so close because of it being a full moon?\u201d\n\nWhat if the moon was not just a physical object but also something that has \u2018a real mind\u2019 and could remember past events, could you imagine what it would be like to actually meet with it face to face"
         }
      ],
      [
         {
            "generated_text":"Right now is the perfect time to look for a job. It\u2019s getting cold and you don\u2019t want to be stuck in the office every day when it\u2019s below 40 degrees. Plus, there are so many opportunities out there that it can feel overwhelming trying to find one.\n\nIf you\u2019re looking to get back into the work force after taking some time off or just starting your career with a new company, there are a ton of benefits from going through"
         }
      ],
      [
         {
            "generated_text":"The one thing I will never regret is my time with him.\n\nI\u2019m not going to write an essay about how I feel, or the things I wish were different. Because, it\u2019s just that \u2013 \u201cthings.\u201d Things like a few hundred thousand more books in his library, or more money (because he didn\u2019t have any). Or better yet, a new house and garden for me and our dog."
         }
      ],
      [
         {
            "generated_text":"The secret to a happy life is to be kind whenever possible. It's an easy thing for people to forget, but we all know that what goes around comes back around, so kindness needs to start from the bottom up. I've been thinking about this lately because I was really mean today in a rather heated discussion. My first instinct was to go straight to being as mean as possible by saying \"I'm sorry you had such a bad day\" or something similar...not nice! But then it"
         }
      ]
   ]
}
```

{% hint style="info" %}
**Note**

GPT-J-6B processes each sentence from a single query one by one. The overall time of the query, however, is slightly shorter than querying each sentence separately.
{% endhint %}

## Few-Shot Learning examples

Few-Shot Learning (sometimes called FSL) is a method where predictions are made based on a low number of training samples. An FSL approach may be applied to GPT-J-6B. In this framework, each query requires a few examples given in a specific format, so that GPT-J can understand what is expected.

In addition to regular text generation, we can use GPT-J-6B for different tasks, for which a few examples are provided:

| [Sentiment analysis](gpt-j-6b.md#sentiment-analysis)                                          |
| --------------------------------------------------------------------------------------------- |
| [Computer language code generation](gpt-j-6b.md#sql-code-generation) (e.g. SQL, Python, HTML) |
| Entity identification                                                                         |
| Question Answering                                                                            |
| Machine language translation                                                                  |
| Chatbot                                                                                       |
| Semantic similarities                                                                         |
| Intent classification                                                                         |

Here are a few examples of Few-Shot Learning mechanisms.

{% hint style="info" %}
**Note**

The output may be different each time we query Inference Service, even when using the same input.
{% endhint %}

### Sentiment analysis

Given the query...

{% code overflow="wrap" %}
```bash
$ curl -d '{"parameters": {"min_length":50,"max_length":100}, "instances": ["Message: The last show was terrible. Sentiment: Negative, Message: I feel great this morning.Sentiment: Positive, Message: GPT-J has 6 billion parameters.Sentiment: Neutral, Message: It was my all-time favorite movie.Sentiment:"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predic
```
{% endcode %}

...this output is returned:

{% code overflow="wrap" %}
```json
{"predictions": [{"generated_text": "Message: The last show was terrible. Sentiment: Negative, Message: I feel great this morning.Sentiment: Positive, Message: GPT-J has 6 billion parameters.Sentiment: Neutral, Message: It was my all-time favorite movie.Sentiment: Positive, Message: I miss seeing old friends on Sundays.Sentiment: Negative, Message: Why did my phone die today? Sentiment: Positive, Message: What a nice surprise! This is awesome!Sentiment"}]}
```
{% endcode %}

**Result:** `Positive`

### SQL code generation

Given the query...

{% code overflow="wrap" %}
```bash
curl -d '{"parameters": {"min_length":50,"max_length":250}, "instances": ["Question: Select teams that have less than 3 developers in it.Answer: SELECT TEAM, COUNT(DEVELOPER) FROM team GROUP BY TEAM HAVING COUNT(DEVELOPER) < 3;Question: Show all teams along with the number of developers in each team, Answer: SELECT TEAM, COUNT(TEAM) FROM team GROUP BY TEAM;Question: Show the recent hired developer, Answer: SELECT * FROM team ORDER BY ID DESC LIMIT 1;Question: Fetch the first three developers from team table;Answer:"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predic
```
{% endcode %}

...this output is returned:

{% code overflow="wrap" %}
```json
{"predictions": [{"generated_text": "Question: Select teams that have less than 3 developers in it.Answer: SELECT TEAM, COUNT(DEVELOPER) FROM team GROUP BY TEAM HAVING COUNT(DEVELOPER) < 3;Question: Show all teams along with the number of developers in each team, Answer: SELECT TEAM, COUNT(TEAM) FROM team GROUP BY TEAM;Question: Show the recent hired developer, Answer: SELECT * FROM team ORDER BY ID DESC LIMIT 1;Question: Fetch the first three developers from team table;Answer: SELECT TEAM, DEV_NAME, DEV_EMAIL FROM team ORDER BY DEV_NAME ASC LIMIT 0,3\n    \"\"\"\n    __sql = {'SELECT': [f\"{t}.*\", f\"{t}.id AS `{key}`\"] for t, key in _table}\n\n    return __sql + list(_sub_sql())\n\n\ndef sub_query_count(*args):\n    def _get_count():\n        count = 0\n        sql = []\n        for"}]}
```
{% endcode %}

**The answer**: `SELECT TEAM, DEV_NAME, DEV_EMAIL FROM team ORDER BY DEV_NAME ASC LIMIT 0,3`

## Parameters

### **General**

<table><thead><tr><th width="353">Parameter</th><th>Description</th></tr></thead><tbody><tr><td><code>GPU</code></td><td>Select the proper GPU model. GPT-J-6B should fit into 16GB of VRAM. See <a href="../../../../../coreweave-kubernetes/node-types.md#component-availability">Node Types</a> for a full list of available labels.</td></tr></tbody></table>

### **Model parameters**

<table><thead><tr><th width="351">Parameter</th><th>Description</th></tr></thead><tbody><tr><td><code>Precision.native</code></td><td>Uses the native model's precision.</td></tr><tr><td><code>Precision.ftp16</code></td><td>Increases the performance and occupies less memory in GPU.</td></tr><tr><td><code>Precision.bfloat16</code></td><td>Increases the precession and occupies less memory in GPU. <code>bfloat16</code> provides better accuracy on Ampere platforms but can not be used on Turing or Volta. Please use <code>fp16</code> on those platforms.</td></tr><tr><td><code>min_length</code></td><td>A minimum number of tokens to generate.</td></tr><tr><td><code>max_length</code></td><td>A maximum number of tokens to generate. (<strong>Note:</strong> The maximum number of tokens for GPT-J-6B is 2048. Usually, the number of tokens is greater than the number of words. See <a href="https://huggingface.co/transformers/tokenizer_summary.html">Summary of the tokenizers</a> for more details.)</td></tr><tr><td><code>temperature</code></td><td>Controls the randomness of the response. A lower value means that the model generates a more deterministic output. A higher value means more explorative and risky output.</td></tr><tr><td><code>top_k</code></td><td>GPT-J-6B generates several attempts to complete a prompt, and it assigns different probabilities to each attempt. <code>top_k</code> describes the number of the most likely attempts.</td></tr><tr><td><code>top_p</code></td><td>It is an alternative method to <code>temperature</code>. A lower value means more likely and safe tokens, and a higher value returns more creative tokens.</td></tr><tr><td><code>repetition_penalty</code></td><td>Avoids sentences that repeat themselves without anything really interesting.</td></tr></tbody></table>

### **Inference service setup**

<table><thead><tr><th width="350">Parameter</th><th>Description</th></tr></thead><tbody><tr><td><code>minReplicas</code></td><td>A number of minimum replicas, when 0, allows scaling to zero serving pods. Scale replicas up may take a few minutes before the service is fully ready.</td></tr><tr><td><code>maxReplicas</code></td><td>A number of maximum replicas</td></tr><tr><td><code>scaleToZeroPodRetentionPeriod</code></td><td>The minimum amount of time that the last pod remains active after the Autoscaler decides to scale pods to zero.</td></tr></tbody></table>

### **Cache parameters**

<table><thead><tr><th width="353">Parameter</th><th>Description</th></tr></thead><tbody><tr><td><code>Disk size</code></td><td>The size of created PVC disk that stores the model and tokenizer.</td></tr></tbody></table>

## Benchmark

The option allows running a benchmark in a separate job. The benchmark runs a loop of batches from 1 up to `batch size`. Each step samples different lengths of tokens from 128 to 2048 in steps of 128.

### **Benchmark parameters**

<table><thead><tr><th width="359">Parameter</th><th>Description</th></tr></thead><tbody><tr><td><code>Batch size</code></td><td>The maximum number of generations in a single query. The bigger batch, the more VRAM occupies. When 0, the benchmark won't start.</td></tr><tr><td><code>Warmup rounds</code></td><td>Run an additional number of warmups before the benchmark.</td></tr><tr><td><code>Benchmark</code> <code>only</code></td><td>When set, the application does not start the Inference Service, only the benchmark.</td></tr></tbody></table>

The following table contains the data for responses of the GPT-J6B model for various sequence lengths per second for half precision (`fp16`). Brain Floating Point (`bfloat16`) precision has the same performance as `fp16`, but offers higher accuracy. It is not available on Turing and Volta architectures.

| Sequence length | V100   | Quadro RTX5000 | RTX A5000 | A40   | A100  | A100  |
| --------------- | ------ | -------------- | --------- | ----- | ----- | ----- |
| 128             | 9.13   | 8.94           | 5.62      | 6.98  | 5.11  | 4.95  |
| 256             | 16.2   | 16.95          | 9.74      | 12.09 | 8.9   | 8.52  |
| 384             | 23.65  | 22.64          | 14.17     | 17.47 | 12.89 | 12.3  |
| 512             | 31.38  | 30.03          | 17.97     | 22.32 | 16.47 | 15.74 |
| 640             | 39.43  | 36.91          | 22.27     | 27.34 | 20.2  | 19.51 |
| 768             | 50.27  | 43.9           | 28.09     | 34.12 | 25.11 | 24.36 |
| 896             | 58.68  | 49.04          | 30.85     | 38.07 | 28.06 | 27.36 |
| 1024            | 68.8   | 55.9           | 35.24     | 43.66 | 32.05 | 30.9  |
| 1152            | 78.45  | 61.84          | 39.02     | 48.28 | 35.36 | 34.37 |
| 1280            | 91.08  | 73.12          | 45.18     | 56.07 | 41.26 | 39.79 |
| 1408            | 101.32 | 85.47          | 53.98     | 61.04 | 45.11 | 43.05 |
| 1536            | 111.21 | 91.93          | 54.22     | 66.3  | 49.69 | 47.86 |
| 1664            | 119.76 | 94.35          | 58        | 71.78 | 53.14 | 51.18 |
| 1792            | 131.12 | 100.37         | 63.14     | 77.5  | 58.04 | 55.26 |
| 1920            | 136.66 | 101.83         | 63.7      | 78.72 | 58.52 | 55.96 |
| 2048            | 149.16 | 110.88         | 69.48     | 85.18 | 63.41 | 61.06 |
