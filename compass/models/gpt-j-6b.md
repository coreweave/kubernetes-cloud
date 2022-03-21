# GPT-J-6B

GPT-J-6B is a 6 billion parameters transformer created by Ben Wang, Aran Komatsuzaki and the team at [Eleuther AI](https://www.eleuther.ai). GPT-J-6B is an open-source alternative to OpenAI's GPT-3 and performs nearly as well as a 6.7B GPT-3 called Curie on various zero-shot down-streaming tasks.

The model was trained on [the Pile](https://arxiv.org/pdf/2101.00027.pdf), a 825GiB dataset from a mixture of sources like academic, internet, prose, dialogue, and different fields, like medicine, programming research, law.

## Installing Inference Service

1.  After logging into [CoreWeave Cloud](https://cloud.coreweave.com), go to CoreWeave Apps `Catalog`

    ![](https://gblobscdn.gitbook.com/assets%2F-M83TghsCfsi8FCYs2DZ%2F-Mj8bRkoZHQnzaZ64weP%2F-Mj8dNozNioSsymBNIg9%2Fimage.png?alt=media\&token=d56bb42a-0572-40ba-b053-4320528a4b25)
2.  A new window opens to CoreWeave Apps with the list of available applications. Find and select the **gpt-j-6b** application

    ![](<../../.gitbook/assets/image (75).png>)\\
3. In the right upper corner, select the latest version of the helm chart and click `DEPLOY`
4. The deployment's form prompts you to enter an application name. The remaining parameters have our suggested defaults; when ready, click `DEPLOY` at the bottom of the page.
5. It takes a few minutes before the deployment is ready.

## Uninstalling

1. In order to delete the Inference Service, log in to [CoreWeave Cloud](https://cloud.coreweave.com), go to CoreWeave Apps `Application.`\\
2. A new window opens with a list of running applications; find the application you want to delete and click `DELETE` button, and then confirm.

{% hint style="info" %}
CoreWeave Clouds removes most of the Kubernetes resources automatically. The following need to be deleted manually:\
\- benchmark job\
\- disk PVC
{% endhint %}

## Accessing Inference Service

{% hint style="info" %}
In order to access Inference Service from the command line, it is necessary to generate and download Kubeconfig. See [Getting Started](https://docs.coreweave.com/coreweave-kubernetes/) for more details.
{% endhint %}

1.  Verify if Inference Service is ready:

    ```
    $ kubectl get isvc
    NAME          URL                                                          READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION                   AGE
    gpt-j-6b-my   http://gpt-j-6b-my.namespace.knative.chi.coreweave.com   True           100                              gpt-j-6b-my-predictor-default-00001   48m
    ```
2.  Once it is ready, copy and paste the `URL` into the query command:

    ```
    curl -d '{"parameters": {"min_length":150,"max_length":200}, "instances": ["In a shocking finding, scientist discovered a herd of unicorns living in a remote, previously unexplored valley"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predict
    ```

**The output**:

> `What's even more surprising, is that there was no indication from any of the villagers or scientists that they had ever seen one before! \nAhem. I'm sorry to tell you this, but I think the game has ended. There are no other possible moves left on your turn. The only remaining possibility for you to move would be to roll a 6, which will end your turn and cause both computers to stop playing immediately as well. If you're playing with real people, they'll need to make their own best guesses when rolling these dice in the future, but if it's just you and the computer, it won't matter.\nThe machine should have finished the first level by now, and so far it hasn't. As soon as you get a new tile on the board, it starts placing another piece right next to the existing piece. You can see it`

{% hint style="info" %}
Each query can be parameterized with the following parameters:\
\- `min_length`\
\- `max_length`\
\- `temperature`\
\- `top_k`\
\-`top_p`\
\-`repetition_penalty`

See [Parameters](https://docs.coreweave.com/compass/models/gpt-j-6b#parameters) for the full description
{% endhint %}

## Batch Processing

The Inference Service allows running multiple inputs in a single query. Batching requests can significantly improve throughput.

For batch processing, we have to pass sentences in `instances` the array:

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

The full `curl` command is:

```bash
curl -d '{"parameters": {"min_length":50,"max_length":100}, "instances": ["Everytime I look to the sky, I always think", "Right now is the perfect time to", "The one thing I will never regret is", "The secret to a happy life is to"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predict
```

Inference Service returns `generated_text` for each sentece from batch, the formatted output for our query is:

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
`The block Parameters` are optional and overwrite defaults from Inference Service are created.
{% endhint %}

{% hint style="info" %}
GPT-J-6B processes each sentence from a single query one by one. The overall time of the query, however, is slightly lower than querying each sentence separately.
{% endhint %}

## Few-Shot Learning Examples

Few-shot attempts to learn new tasks provided only a handful of training examples. Each query requires a few examples in a specific format so that GPT-J can understand what we expect.

Besides regular text generation, we can use GPT-J-6B for different tasks:

* Sentiment Analysis
* Computer languages code generation, e.g. SQL, Python, HTML
* Entity identification
* Question Answering
* Machine language translation
* Chatbot
* Semantic similarities
* Intent classification

In the next section, we present just a few examples of few-shot learning mechanisms.

{% hint style="info" %}
The output may be different each time we query Inference Service with the same input.
{% endhint %}

### Sentiment analysis

```bash
$ curl -d '{"parameters": {"min_length":50,"max_length":100}, "instances": ["Message: The last show was terrible. Sentiment: Negative, Message: I feel great this morning.Sentiment: Positive, Message: GPT-J has 6 billion parameters.Sentiment: Neutral, Message: It was my all-time favorite movie.Sentiment:"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predic

{"predictions": [{"generated_text": "Message: The last show was terrible. Sentiment: Negative, Message: I feel great this morning.Sentiment: Positive, Message: GPT-J has 6 billion parameters.Sentiment: Neutral, Message: It was my all-time favorite movie.Sentiment: Positive, Message: I miss seeing old friends on Sundays.Sentiment: Negative, Message: Why did my phone die today? Sentiment: Positive, Message: What a nice surprise! This is awesome!Sentiment"}]}
```

**The answer**: `Positive`

### SQL Code Generation

```bash
curl -d '{"parameters": {"min_length":50,"max_length":250}, "instances": ["Question: Select teams that have less than 3 developers in it.Answer: SELECT TEAM, COUNT(DEVELOPER) FROM team GROUP BY TEAM HAVING COUNT(DEVELOPER) < 3;Question: Show all teams along with the number of developers in each team, Answer: SELECT TEAM, COUNT(TEAM) FROM team GROUP BY TEAM;Question: Show the recent hired developer, Answer: SELECT * FROM team ORDER BY ID DESC LIMIT 1;Question: Fetch the first three developers from team table;Answer:"]}' <URL>/v1/models/eleutherai-gpt-j-6b:predic

{"predictions": [{"generated_text": "Question: Select teams that have less than 3 developers in it.Answer: SELECT TEAM, COUNT(DEVELOPER) FROM team GROUP BY TEAM HAVING COUNT(DEVELOPER) < 3;Question: Show all teams along with the number of developers in each team, Answer: SELECT TEAM, COUNT(TEAM) FROM team GROUP BY TEAM;Question: Show the recent hired developer, Answer: SELECT * FROM team ORDER BY ID DESC LIMIT 1;Question: Fetch the first three developers from team table;Answer: SELECT TEAM, DEV_NAME, DEV_EMAIL FROM team ORDER BY DEV_NAME ASC LIMIT 0,3\n    \"\"\"\n    __sql = {'SELECT': [f\"{t}.*\", f\"{t}.id AS `{key}`\"] for t, key in _table}\n\n    return __sql + list(_sub_sql())\n\n\ndef sub_query_count(*args):\n    def _get_count():\n        count = 0\n        sql = []\n        for"}]}
```

**The answer**: `SELECT TEAM, DEV_NAME, DEV_EMAIL FROM team ORDER BY DEV_NAME ASC LIMIT 0,3`

## Parameters

**General**\\

***

| Parameter | Description                                                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GPU`     | Select the proper GPU model. GPT-J-6B should fit into 16GB of VRAM. See [Node Types](../../coreweave-kubernetes/node-types.md#component-availability) for a full list of available labels. |

**Model Parameters**\\

***

| Parameter            | Description                                                                                                                                                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Precision.`native`   | Uses the native model's precision.                                                                                                                                                              |
| Precision.`ftp16`    | Increases the performance and occupies less memory in GPU.                                                                                                                                      |
| Precision.`bfloat16` | Increases the precession and occupies less memory in GPU. `bfloat16` provides better accuracy on Ampere platforms but can not be used on Turing or Volta. Please use `fp16` on those platforms. |
| `min_length`         | A minimum number of tokens to generate.                                                                                                                                                         |
| `max_length`         | A maximum number of tokens to generate.\[¹]                                                                                                                                                     |
| `temperature`        | Controls the randomness of the response. A lower value means that the model generates a more deterministic output. A higher value means more explorative and risky output.                      |
| `top_k`              | GPT-J-6B generates several attempts to complete a prompt, and it assigns different probabilities to each attempt. `top_k` describes the number of the most likely attempts.                     |
| `top_p`              | It is an alternative method to `temperature`. A lower value means more likely and safe tokens, and a higher value returns more creative tokens.                                                 |
| `repetition_penalty` | Avoids sentences that repeat themselves without anything really interesting.                                                                                                                    |

{% hint style="info" %}
\[¹] - The maximum number of tokens for GPT-J-6B is 2048. Usually, the number of tokens is greater than the number of words. See [Summary of the tokenizers](https://huggingface.co/transformers/tokenizer\_summary.html) for more details.
{% endhint %}

**Inference Service Setup**

| Parameter                       | Description                                                                                                                                            |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `minReplicas`                   | A number of minimum replicas, when 0, allows scaling to zero serving pods. Scale replicas up may take a few minutes before the service is fully ready. |
| `maxReplicas`                   | A number of maximum replicas                                                                                                                           |
| `scaleToZeroPodRetentionPeriod` | The minimum amount of time that the last pod remains active after the Autoscaler decides to scale pods to zero.                                        |

**Benchmark**

The option allows running a benchmark in a separate job. Benchmark runs a loop of batches from 1 up to `batch size`. Each step samples different lengths of tokens from 128 to 2048 in steps of 128.

| Parameter          | Description                                                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `Batch size`       | The maximum number of generations in a single query. The bigger batch, the more VRAM occupies. When 0, the benchmark won't start. |
| `Warmup rounds`    | Run an additional number of warmups before the benchmark.                                                                         |
| `Benchmark` `only` | When set, the application does not start the Inference Service, only the benchmark.                                               |

{% hint style="info" %}
We already prepared a [benchmark](gpt-j-6b.md#benchmark) for different types of GPUs
{% endhint %}

**Cache Parameters**

| Parameter   | Description                                                       |
| ----------- | ----------------------------------------------------------------- |
| `Disk size` | The size of created PVC disk that stores the model and tokenizer. |

## Benchmark

The table shows responses of the GPT-J6B for various sequence lengths per second for half precision (fp16). Brain Floating Point (bfloat16) precision has the same performance as fp16 but better accuracy and it is not available on Turing and Volta architectures.

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
