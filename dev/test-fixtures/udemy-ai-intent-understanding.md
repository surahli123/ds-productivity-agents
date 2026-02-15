# Source: https://medium.com/udemy-engineering/evolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364

[Sitemap](/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](/?source=post_page---top_nav_layout_nav-----------------------------------------)

[Write](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

## [Udemy Tech Blog](https://medium.com/udemy-engineering?source=post_page---publication_nav-19c6d3367ed4-ec3ee0039364---------------------------------------)

·

Follow publication

[![Udemy Tech Blog](https://miro.medium.com/v2/resize:fill:38:38/1*Ygluf48GlOqiN_ptp-OwZQ.png)](https://medium.com/udemy-engineering?source=post_page---post_publication_sidebar-19c6d3367ed4-ec3ee0039364---------------------------------------)

Learn about cool projects, product initiatives, and company culture from the data science and engineering teams at Udemy. Find these projects fun? We’re hiring! <https://about.udemy.com/careers/>

Follow publication

# **Evolution of the Udemy AI Assistant Intent Understanding System**

[![Jack Kwok](https://miro.medium.com/v2/resize:fill:32:32/1*ovjKiuvw64MWK8JNdENuKg.jpeg)](/@planetai?source=post_page---byline--ec3ee0039364---------------------------------------)

[Jack Kwok](/@planetai?source=post_page---byline--ec3ee0039364---------------------------------------)

Follow

8 min read

·

May 28, 2025

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fudemy-engineering%2Fec3ee0039364&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&user=Jack+Kwok&userId=58c705f9c552&source=---header_actions--ec3ee0039364---------------------clap_footer------------------)

504

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fec3ee0039364&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&source=---header_actions--ec3ee0039364---------------------bookmark_footer------------------)

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dec3ee0039364&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&source=---header_actions--ec3ee0039364---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/1*rP4bbWcE-vZY-w5Cr1uNQQ.png)

**Introduction**

Imagine having a virtual learning companion by your side every time you tackle a new course or challenging concept‌, ‌ready to clarify doubts, summarize lessons, or quiz your understanding on demand. This isn’t just an idea for the future. Thanks to the Udemy AI Assistant, it’s a reality for every Udemy learner today. Powered by AI, the Assistant is actively supporting learners all over the world, guiding them step by step through their skills development journeys and making learning smoother, faster, and more personalized than ever.

Behind the scenes, delivering such smart, relevant help relies on one crucial ability: understanding exactly what the learner wants. From course-related clarifications to lecture summaries and beyond, the AI Assistant must accurately grasp the intent behind every question to deliver the perfect response.

In this article, we’ll take you behind the curtain to explore how we’ve evolved the Udemy AI Assistant’s intent understanding system. You’ll discover key lessons from our journey: the challenges we faced as we expanded features, breakthroughs that boosted accuracy, and how we balanced response quality, speed, and cost.

**Background**

With Large Language Models (LLMs), setting the relevant context in the prompt is key to eliciting high-quality, high-relevance chat responses. To that end, we enable the AI Assistant to connect to various data sources and services to obtain the most relevant context. Behind the scenes, the AI Assistant predicts the learner’s intent and then invokes the corresponding chain of actions to fetch the most helpful context from data sources and APIs. For example, if the learner intends to ask for a summary of the current video lecture, a chain of actions would include invoking an API call to fetch the pre-generated lecture summary and send it to the LLM for final response generation. As another example, if the learner intends to search for a topic within the course, a function call will execute a search through our internal Search API. With this architecture, the intent understanding system has the important role of determining the chain of actions downstream. An incorrect intent classification often results in an incorrect response, as demonstrated in the following conversation:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*4cF542hkS3zpaoJN)

Incorrect AI Assistant response: A misclassified intent triggered a lecture search action. The expected action is lecture summarization.

**Initial approach**

When a learner submits a message, the first step is to predict the learner’s intent. In the initial version of the AI Assistant, we utilized a basic similarity-based approach to predict the intent. Using Nvidia’s open-sourced NeMo Guardrails package, we predefined a set of “user intents” each with sample user utterances (e.g., “Can you summarize the main ideas of this lecture?” can be a sample utterance for the lecture summarization intent). The sample user utterances are embedded and saved into a lightweight vector database. After the learner submits a message, the most similar embedding, based on cosine distance and approximate nearest neighbor, is retrieved. The system predicts the user intent solely based on the closest matching user utterance in the database. At the initial product launch, the lightweight sentence embedding model all-MiniLM-L6-v2 was used to embed the learner’s messages. With this small model, embedding operations were swift and incurred negligible inference costs.

Following the release, new AI Assistant features were implemented which required understanding additional intents. As we scaled out to new intents, we noticed a degradation in AI Assistant response quality. Using data collected from the AI Assistant response quality feedback, we analyzed patterns of incorrect responses, which we attributed to incorrect intent classification. It became apparent that classification confusion increased after additional intents were added. Adding more sample utterances only slightly mitigated the problem.

**Tackling response quality**

Once we have identified intent misclassification as the root cause of low response quality, we set out to examine the existing approach and research methods to improve its accuracy.

Regarding evaluating new approaches, our key considerations are:

  * Response Quality
  * Inference Cost
  * Response Latency

**Larger and better embedding model**

We decided to run evaluations on available open-weight embedding models. The diagram shows the accuracy comparison on an early version of our test set:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*vNkHOpqKw-MB1mA7)

Diagram 1: Performance on early version of our test set

It was evident that multilingual-e5-base gave us the best performance/cost ratio. _Multilingual-e5-base_ (278M params) requires approximately an order of magnitude more FLOPs than _all-MiniLM-L6-v2_ (23M params). So we decided to deploy the embedding model to a standalone service. This new model also gave us the benefit of multilingual support as we expanded support to more and more languages.

The larger embedding model gave us the needed boost in response quality immediately. However, the boost was lost over time as we added a few new intents to support new features. Specifically, we noticed a high percentage of false positive classifications for the new lecture search user intent (see Example 1).

To better estimate up-to-date intent classification performance, we expanded our test set to cover old and new user intents, then re-ran the evaluation. The results confirmed a big gap in intent classification performance.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*Z481c-Q1EjqUoOu2)

Diagram 2: Perfomance on our expanded test set

This led us to revisit our approach.

**Experiment: fine-tuning the embedding model with hard negatives**

For this experiment, the hypothesis was that the off-the-shelf multilingual-e5-base struggled to capture the nuances of our learners’ messages. The off-the-shelf models were trained to perform well on generic natural language processing tasks. Two sentences considered semantically similar in the general sense may not necessarily carry the same meaning in our learning-focused use cases. By fine-tuning the model with a sufficiently large number of actual misclassified messages in a process called hard negative mining, we hoped the fine-tuned model would learn the nuances in our learners’ messages.

Unfortunately, after many experimental trials using different embedding models and different loss functions, the metrics showed no improvement. We decided to try another approach.

**LLM-only approach**

The embedding approach had two major limitations. First, we observed a high level of confusion for certain intents. For instance, messages mentioning “lecture” were often misclassified as lecture search instead of the correct intent, such as lecture summarization. We hypothesized that the sentence embedding process acted as a form of lossy compression where key semantic information was sometimes lost. The second limitation was that our embedding approach considered only the most recent learner message due to the small, fixed input size of embedding models (768 tokens for multilingual-e5-base). It was not capable of considering the totality of the conversation. To tackle those two limitations together, we decided to leverage an LLM to take as input the chat history to predict the learner’s intent. Our hypothesis was that even a small LLM should be able to perform better than our best embedding model.

We evaluated these LLMs on costs, latency, and classification performance:

  * gpt-4.1
  * gpt-4.1-mini
  * gpt-4.1-nano

Here we showed the performance of the LLM-only approach using various LLM models at our disposal.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*H2fJrfYcn37w7Qt6)

Diagram 3: LLM-only Performance

In our evaluations, gpt-4.1-nano performed slightly better than gpt-4.1-mini but cost ~75% less than gpt-4.1-mini. gpt-4.1-nano had the lowest latency among the three models. gpt-4.1-nano was the clear winner.

Again, the key to eliciting a good LLM response is providing good context. We utilized a few-shot learning approach by providing a few examples per user intent in our custom user intent classification prompt.

## Get Jack Kwok’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Here is a snippet of our user intent classification prompt:

> You must determine the user intent. Always return one of the predefined user intents:
> 
> asks course question
> 
> asks course overview question
> 
> searches lecture
> 
> asks lecture summarization
> 
> …
> 
> Never come up with a new intent. Use English only.
> 
> The user intent responses from the Bot are the complete set of predefined user intents.
> 
> User
> 
> What is a recursive function and when should it be used?
> 
> Bot
> 
> User intent: asks course question
> 
> User
> 
> What are the key components of a successful business operations strategy?
> 
> Bot
> 
> User intent: asks course question
> 
> User
> 
> what is covered in this course?
> 
> Bot
> 
> User intent: asks course overview question
> 
> User
> 
> which lecture talks about recursion?
> 
> Bot
> 
> User intent: searches lecture

We observed a ~19 percentage point increase in classification accuracy compared to the embedding-only approach.

However, this approach comes with two drawbacks. It adds an average additional latency of 0.6 seconds to each chat response. The extra _gpt-4.1-nano_ call results in a 10% increase in overall LLM costs per conversation.

**The final hybrid approach**

While the LLM-only approach showed a leap in classification performance, we didn’t want to ignore the extra OpenAI roundtrip latency, which may hurt the user experience. So we decided to experiment with a hybrid approach.

For each learner message, we retrieved the most similar embedding from the vector database. If the similarity score exceeded a pre-set threshold, we use the most similar embedding to predict the learner’s intent. Otherwise, invoke the LLM to make the prediction.

We approximated the optimal threshold by running metrics on the validation set across a range of thresholds at 0.05 increments:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*HAzYV6-nSIoe5wkv)

Diagram 4: Threshold optimization

In the case of _gpt-4.1-nano_ , the estimated optimal threshold is 0.85. We then ran a similar threshold analysis on _gpt-4.1-mini_ and gpt-4.1 models and obtained these results for comparison.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*jpnlDsETkzwpkXM7)

Diagram 5: Hybrid Embedding + LLM Performance

When performing a classification task, the LLM response was very short (<10 output tokens) so we considered only input token costs for simplicity:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*sgOXa9zgJcqebH63)

Diagram 6: Cost Comparisons among gpt-4.1 variants

While _gpt-4.1_ outperforms _gpt-4.1-nano_ by a 3% margin, it costs 20x more. _gpt-4.1-nano_ is the obvious winner from a performance-to-cost perspective.

Regarding the additional response generation latency, the _gpt-4.1-nano_ call required an averaged ~0.6s roundtrip. This extra roundtrip increased the end-to-end response average latency by ~10%, which was still an acceptable latency. In addition, we estimated only 32.5% of all learner messages triggered the _gpt-4.1-nano_ fallback.

Finally, we tested the hybrid solution on the failed conversation from earlier:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*sLTNovaDx8ufa4od)

Correct AI Assistant response

**Conclusion**

In summary, we achieved the best of both worlds with this hybrid approach. The AI Assistant achieves high accuracy with only a small increase in latency and cost. We plan to monitor ‌learners’ feedback to validate the impact on learner satisfaction. Going forward, we plan to continue to add new and powerful capabilities into the AI Assistant to make it even more helpful to all Udemy learners.

[Udemy](/tag/udemy?source=post_page-----ec3ee0039364---------------------------------------)

[Chatbots](/tag/chatbots?source=post_page-----ec3ee0039364---------------------------------------)

[LLM](/tag/llm?source=post_page-----ec3ee0039364---------------------------------------)

[AI](/tag/ai?source=post_page-----ec3ee0039364---------------------------------------)

[Artificial Intelligence](/tag/artificial-intelligence?source=post_page-----ec3ee0039364---------------------------------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fudemy-engineering%2Fec3ee0039364&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&user=Jack+Kwok&userId=58c705f9c552&source=---footer_actions--ec3ee0039364---------------------clap_footer------------------)

504

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fudemy-engineering%2Fec3ee0039364&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&user=Jack+Kwok&userId=58c705f9c552&source=---footer_actions--ec3ee0039364---------------------clap_footer------------------)

504

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fec3ee0039364&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&source=---footer_actions--ec3ee0039364---------------------bookmark_footer------------------)

[![Udemy Tech Blog](https://miro.medium.com/v2/resize:fill:48:48/1*Ygluf48GlOqiN_ptp-OwZQ.png)](https://medium.com/udemy-engineering?source=post_page---post_publication_info--ec3ee0039364---------------------------------------)

[![Udemy Tech Blog](https://miro.medium.com/v2/resize:fill:64:64/1*Ygluf48GlOqiN_ptp-OwZQ.png)](https://medium.com/udemy-engineering?source=post_page---post_publication_info--ec3ee0039364---------------------------------------)

Follow

## [Published in Udemy Tech Blog](https://medium.com/udemy-engineering?source=post_page---post_publication_info--ec3ee0039364---------------------------------------)

[1.4K followers](/udemy-engineering/followers?source=post_page---post_publication_info--ec3ee0039364---------------------------------------)

·[Last published Sep 22, 2025](/udemy-engineering/from-zero-to-hero-localization-led-generative-ai-at-udemy-a422e4f968d4?source=post_page---post_publication_info--ec3ee0039364---------------------------------------)

Learn about cool projects, product initiatives, and company culture from the data science and engineering teams at Udemy. Find these projects fun? We’re hiring! <https://about.udemy.com/careers/>

Follow

[![Jack Kwok](https://miro.medium.com/v2/resize:fill:48:48/1*ovjKiuvw64MWK8JNdENuKg.jpeg)](/@planetai?source=post_page---post_author_info--ec3ee0039364---------------------------------------)

[![Jack Kwok](https://miro.medium.com/v2/resize:fill:64:64/1*ovjKiuvw64MWK8JNdENuKg.jpeg)](/@planetai?source=post_page---post_author_info--ec3ee0039364---------------------------------------)

Follow

## [Written by Jack Kwok](/@planetai?source=post_page---post_author_info--ec3ee0039364---------------------------------------)

[112 followers](/@planetai/followers?source=post_page---post_author_info--ec3ee0039364---------------------------------------)

·[56 following](/@planetai/following?source=post_page---post_author_info--ec3ee0039364---------------------------------------)

Engineer-Scientist specialized in applying Artificial Intelligence in Healthcare, Robotics, and Education.

Follow

## No responses yet

[](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page---post_responses--ec3ee0039364---------------------------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fevolution-of-the-udemy-ai-assistant-intent-understanding-system-ec3ee0039364&source=---post_responses--ec3ee0039364---------------------respond_sidebar------------------)

Cancel

Respond

## More from Jack Kwok and Udemy Tech Blog

![Deep Learning for Disaster Recovery](https://miro.medium.com/v2/resize:fit:679/format:webp/1*oW08mGSEKTonwVgT7BXuTw.png)

[![Insight](https://miro.medium.com/v2/resize:fill:20:20/1*bVN8Kd_RsjRN8JuKIc6U0w.png)](https://medium.com/insight-data?source=post_page---author_recirc--ec3ee0039364----0---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

In

[Insight](https://medium.com/insight-data?source=post_page---author_recirc--ec3ee0039364----0---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

by

[Jack Kwok](/@planetai?source=post_page---author_recirc--ec3ee0039364----0---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

## [Deep Learning for Disaster RecoveryAutomatic Detection of Flooded Roads](/insight-data/deep-learning-for-disaster-recovery-45c8cd174d7a?source=post_page---author_recirc--ec3ee0039364----0---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

Dec 15, 2017

[A clap icon722A response icon2](/insight-data/deep-learning-for-disaster-recovery-45c8cd174d7a?source=post_page---author_recirc--ec3ee0039364----0---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F45c8cd174d7a&operation=register&redirect=https%3A%2F%2Fmedium.com%2Finsight-data%2Fdeep-learning-for-disaster-recovery-45c8cd174d7a&source=---author_recirc--ec3ee0039364----0-----------------bookmark_preview----325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

![Building a Multi-Armed Bandit System from the Ground Up: A Recommendations and Ranking Case Study…](https://miro.medium.com/v2/resize:fit:679/format:webp/1*QtG3PRxhrP-BkB6bO6aVgw.png)

[![Udemy Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*Ygluf48GlOqiN_ptp-OwZQ.png)](https://medium.com/udemy-engineering?source=post_page---author_recirc--ec3ee0039364----1---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

In

[Udemy Tech Blog](https://medium.com/udemy-engineering?source=post_page---author_recirc--ec3ee0039364----1---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

by

[Austin Wang](/@austin.wang_29055?source=post_page---author_recirc--ec3ee0039364----1---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

## [Building a Multi-Armed Bandit System from the Ground Up: A Recommendations and Ranking Case Study…Introduction](/udemy-engineering/building-a-multi-armed-bandit-system-from-the-ground-up-a-recommendations-and-ranking-case-study-b598f1f880e1?source=post_page---author_recirc--ec3ee0039364----1---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

Nov 15, 2022

[A clap icon208A response icon3](/udemy-engineering/building-a-multi-armed-bandit-system-from-the-ground-up-a-recommendations-and-ranking-case-study-b598f1f880e1?source=post_page---author_recirc--ec3ee0039364----1---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fb598f1f880e1&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Fbuilding-a-multi-armed-bandit-system-from-the-ground-up-a-recommendations-and-ranking-case-study-b598f1f880e1&source=---author_recirc--ec3ee0039364----1-----------------bookmark_preview----325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

![From siloed DataOps, MLOps, and LLMOps to a unified data‑intelligence platform](https://miro.medium.com/v2/resize:fit:679/format:webp/0*W6C5SeBr0M7WcDJL)

[![Udemy Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*Ygluf48GlOqiN_ptp-OwZQ.png)](https://medium.com/udemy-engineering?source=post_page---author_recirc--ec3ee0039364----2---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

In

[Udemy Tech Blog](https://medium.com/udemy-engineering?source=post_page---author_recirc--ec3ee0039364----2---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

by

[Rajit Saha](/@saha.rajit?source=post_page---author_recirc--ec3ee0039364----2---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

## [From siloed DataOps, MLOps, and LLMOps to a unified data‑intelligence platformIntroduction](/udemy-engineering/from-siloed-dataops-mlops-and-llmops-to-a-unified-data-intelligence-platform-4400be283641?source=post_page---author_recirc--ec3ee0039364----2---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

Jul 31, 2025

[A clap icon105](/udemy-engineering/from-siloed-dataops-mlops-and-llmops-to-a-unified-data-intelligence-platform-4400be283641?source=post_page---author_recirc--ec3ee0039364----2---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F4400be283641&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Ffrom-siloed-dataops-mlops-and-llmops-to-a-unified-data-intelligence-platform-4400be283641&source=---author_recirc--ec3ee0039364----2-----------------bookmark_preview----325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

![Understanding K-Means Clustering and Kernel Methods](https://miro.medium.com/v2/resize:fit:679/format:webp/1*7yiVuFC7brw9d-cq6hzPHQ.jpeg)

[![Udemy Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*Ygluf48GlOqiN_ptp-OwZQ.png)](https://medium.com/udemy-engineering?source=post_page---author_recirc--ec3ee0039364----3---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

In

[Udemy Tech Blog](https://medium.com/udemy-engineering?source=post_page---author_recirc--ec3ee0039364----3---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

by

[Meltem Tutar](/@meltem.tutar?source=post_page---author_recirc--ec3ee0039364----3---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

## [Understanding K-Means Clustering and Kernel MethodsAt Udemy we use clustering techniques on many projects, especially when we lack labelled data. Here we explain clustering fundamentals](/udemy-engineering/understanding-k-means-clustering-and-kernel-methods-afad4eec3c11?source=post_page---author_recirc--ec3ee0039364----3---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

Sep 8, 2021

[A clap icon151](/udemy-engineering/understanding-k-means-clustering-and-kernel-methods-afad4eec3c11?source=post_page---author_recirc--ec3ee0039364----3---------------------325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fafad4eec3c11&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fudemy-engineering%2Funderstanding-k-means-clustering-and-kernel-methods-afad4eec3c11&source=---author_recirc--ec3ee0039364----3-----------------bookmark_preview----325b3721_d6b6_400e_b6bb_24acdf12db06--------------)

[See all from Jack Kwok](/@planetai?source=post_page---author_recirc--ec3ee0039364---------------------------------------)

[See all from Udemy Tech Blog](https://medium.com/udemy-engineering?source=post_page---author_recirc--ec3ee0039364---------------------------------------)

## Recommended from Medium

![Agentic AI in the Cloud: Comparing AWS, Azure, and GCP for Production-Ready Agent Systems](https://miro.medium.com/v2/resize:fit:679/format:webp/1*u8FNc5v3DqvbWrUiLeogXQ.png)

[![Towards AI](https://miro.medium.com/v2/resize:fill:20:20/1*JyIThO-cLjlChQLb6kSlVQ.png)](https://medium.com/towards-artificial-intelligence?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

In

[Towards AI](https://medium.com/towards-artificial-intelligence?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

by

[Kyle knudson](/@kyle.knudson2015?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

## [Agentic AI in the Cloud: Comparing AWS, Azure, and GCP for Production-Ready Agent SystemsAgentic AI is moving from flashy demos to real production workloads: support bots that triage incidents, “copilot” tools for data…](/towards-artificial-intelligence/agentic-ai-in-the-cloud-comparing-aws-azure-and-gcp-for-production-ready-agent-systems-ee21a7fe8c10?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

Dec 7, 2025

[A clap icon42](/towards-artificial-intelligence/agentic-ai-in-the-cloud-comparing-aws-azure-and-gcp-for-production-ready-agent-systems-ee21a7fe8c10?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fee21a7fe8c10&operation=register&redirect=https%3A%2F%2Fpub.towardsai.net%2Fagentic-ai-in-the-cloud-comparing-aws-azure-and-gcp-for-production-ready-agent-systems-ee21a7fe8c10&source=---read_next_recirc--ec3ee0039364----0-----------------bookmark_preview----7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

![Stanford Just Killed Prompt Engineering With 8 Words \(And I Can’t Believe It Worked\)](https://miro.medium.com/v2/resize:fit:679/format:webp/1*va3sFwIm26snbj5ly9ZsgA.jpeg)

[![Generative AI](https://miro.medium.com/v2/resize:fill:20:20/1*M4RBhIRaSSZB7lXfrGlatA.png)](https://medium.com/generative-ai?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

In

[Generative AI](https://medium.com/generative-ai?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

by

[Adham Khaled](/@adham__khaled__?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

## [Stanford Just Killed Prompt Engineering With 8 Words (And I Can’t Believe It Worked)ChatGPT keeps giving you the same boring response? This new technique unlocks 2× more creativity from ANY AI model — no training required…](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

Oct 19, 2025

[A clap icon23KA response icon618](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F8349d6524d2b&operation=register&redirect=https%3A%2F%2Fgenerativeai.pub%2Fstanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b&source=---read_next_recirc--ec3ee0039364----1-----------------bookmark_preview----7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

![AI Agents: Complete Course](https://miro.medium.com/v2/resize:fit:679/format:webp/1*PvPPSGJ9779FTWmtK_Yeyw.png)

[![Data Science Collective](https://miro.medium.com/v2/resize:fill:20:20/1*0nV0Q-FBHj94Kggq00pG2Q.jpeg)](https://medium.com/data-science-collective?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

In

[Data Science Collective](https://medium.com/data-science-collective?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

by

[Marina Wyss](/@gratitudedriven?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

## [AI Agents: Complete CourseFrom beginner to intermediate to production.](/data-science-collective/ai-agents-complete-course-f226aa4550a1?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

Dec 6, 2025

[A clap icon3.4KA response icon118](/data-science-collective/ai-agents-complete-course-f226aa4550a1?source=post_page---read_next_recirc--ec3ee0039364----0---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ff226aa4550a1&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fdata-science-collective%2Fai-agents-complete-course-f226aa4550a1&source=---read_next_recirc--ec3ee0039364----0-----------------bookmark_preview----7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

![Designing efficient Agentic AI Workflows](https://miro.medium.com/v2/resize:fit:679/format:webp/1*PFs7xcYsnE0YuhRTj96wiw.png)

[![AI Advances](https://miro.medium.com/v2/resize:fill:20:20/1*R8zEd59FDf0l8Re94ImV0Q.png)](https://medium.com/ai-advances?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

In

[AI Advances](https://medium.com/ai-advances?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

by

[Debmalya Biswas](/@debmalyabiswas?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

## [Designing efficient Agentic AI WorkflowsAgentification UI/UX: Mapping Enterprise Processes to Agentic Execution Graphs](/ai-advances/why-designing-efficient-agentic-ai-workflows-is-so-hard-f6ceb07496aa?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

6d ago

[A clap icon281A response icon6](/ai-advances/why-designing-efficient-agentic-ai-workflows-is-so-hard-f6ceb07496aa?source=post_page---read_next_recirc--ec3ee0039364----1---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ff6ceb07496aa&operation=register&redirect=https%3A%2F%2Fai.gopubby.com%2Fwhy-designing-efficient-agentic-ai-workflows-is-so-hard-f6ceb07496aa&source=---read_next_recirc--ec3ee0039364----1-----------------bookmark_preview----7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

![Multi-Agent Systems: Orchestrating AI Agents with A2A Protocol](https://miro.medium.com/v2/resize:fit:679/format:webp/1*H1VmLbqTiTZ6ptMdtITkog.png)

[![Yusuf Baykaloğlu](https://miro.medium.com/v2/resize:fill:20:20/1*rgxJ2vD7Lo4Tf7-dbMBZIQ.jpeg)](/@yusufbaykaloglu?source=post_page---read_next_recirc--ec3ee0039364----2---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[Yusuf Baykaloğlu](/@yusufbaykaloglu?source=post_page---read_next_recirc--ec3ee0039364----2---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

## [Multi-Agent Systems: Orchestrating AI Agents with A2A ProtocolA Deep Dive into Agent Architecture, Workflows, and Real-World Implementation](/@yusufbaykaloglu/multi-agent-systems-orchestrating-ai-agents-with-a2a-protocol-19a27077aed8?source=post_page---read_next_recirc--ec3ee0039364----2---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

Jan 12

[A clap icon120](/@yusufbaykaloglu/multi-agent-systems-orchestrating-ai-agents-with-a2a-protocol-19a27077aed8?source=post_page---read_next_recirc--ec3ee0039364----2---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F19a27077aed8&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40yusufbaykaloglu%2Fmulti-agent-systems-orchestrating-ai-agents-with-a2a-protocol-19a27077aed8&source=---read_next_recirc--ec3ee0039364----2-----------------bookmark_preview----7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

![The Anthropic Hive Mind](https://miro.medium.com/v2/resize:fit:679/format:webp/1*13Lj8DPzU5c3uhYw73LYwg.jpeg)

[![Steve Yegge](https://miro.medium.com/v2/resize:fill:20:20/1*8Ae2b9dv-sQtme8C4_sjhA.jpeg)](/@steve-yegge?source=post_page---read_next_recirc--ec3ee0039364----3---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[Steve Yegge](/@steve-yegge?source=post_page---read_next_recirc--ec3ee0039364----3---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

## [The Anthropic Hive MindAs you’ve probably noticed, something is happening over at Anthropic. They are a spaceship that is beginning to take off.](/@steve-yegge/the-anthropic-hive-mind-d01f768f3d7b?source=post_page---read_next_recirc--ec3ee0039364----3---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

Feb 6

[A clap icon2.1KA response icon56](/@steve-yegge/the-anthropic-hive-mind-d01f768f3d7b?source=post_page---read_next_recirc--ec3ee0039364----3---------------------7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fd01f768f3d7b&operation=register&redirect=https%3A%2F%2Fsteve-yegge.medium.com%2Fthe-anthropic-hive-mind-d01f768f3d7b&source=---read_next_recirc--ec3ee0039364----3-----------------bookmark_preview----7b81ced0_66b2_403a_a86c_3d87aec96279--------------)

[See more recommendations](/?source=post_page---read_next_recirc--ec3ee0039364---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----ec3ee0039364---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----ec3ee0039364---------------------------------------)

[About](/about?autoplay=1&source=post_page-----ec3ee0039364---------------------------------------)

[Careers](/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----ec3ee0039364---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----ec3ee0039364---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----ec3ee0039364---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----ec3ee0039364---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----ec3ee0039364---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----ec3ee0039364---------------------------------------)