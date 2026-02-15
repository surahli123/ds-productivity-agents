# Source: https://medium.com/airbnb-engineering/discovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c

[Sitemap](/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](/?source=post_page---top_nav_layout_nav-----------------------------------------)

[Write](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

## [The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---publication_nav-53c7c27702d5-6a55f5400a0c---------------------------------------)

·

Follow publication

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:38:38/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_sidebar-53c7c27702d5-6a55f5400a0c---------------------------------------)

Creative engineers and data scientists building a world where you can belong anywhere. <http://airbnb.io>

Follow publication

1

Top highlight

# **Discovering and Classifying In-app Message Intent at Airbnb**

## Conversational AI is inspiring us to rethink the customer experience on our platform.

[![Michelle \(Guqian\) Du](https://miro.medium.com/v2/resize:fill:32:32/1*ttzEe83XytaRWhbtABdcFA.jpeg)](/@michelle.du?source=post_page---byline--6a55f5400a0c---------------------------------------)

[Michelle (Guqian) Du](/@michelle.du?source=post_page---byline--6a55f5400a0c---------------------------------------)

Follow

11 min read

·

Jan 22, 2019

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F6a55f5400a0c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&user=Michelle+%28Guqian%29+Du&userId=f81a16adf62&source=---header_actions--6a55f5400a0c---------------------clap_footer------------------)

1.2K

6

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F6a55f5400a0c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&source=---header_actions--6a55f5400a0c---------------------bookmark_footer------------------)

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D6a55f5400a0c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&source=---header_actions--6a55f5400a0c---------------------post_audio_button------------------)

Share

**Authors:** [_Michelle Du_](/@michelle.du) _,_[_Shijing Yao_](/@yaoshijing)

![](https://miro.medium.com/v2/resize:fit:7067/1*e6K-2_rqi8xBjjMEpiFjNA.jpeg) Get embraced by plenty of natural light, brick, and plant in our new office in downtown Seattle.

Airbnb’s mission is to create a world where everyone can belong anywhere. Ensuring good communication between guests and hosts is one of the keys to developing a sense of belonging as well as a smooth and worry-free trip experience for guests. Millions of guests and hosts communicate on the Airbnb messaging platform about a variety of topics, including booking arrangements, payment requests, trip planning, service feedback, and even sharing experiences with new friends. Thus, a huge opportunity to improve the experience for guests on the platform is to predict and understand the intent of their messages to hosts.

Consider the following situation. Christmas is two weeks out. You are planning a last-minute family trip to Hawaii, and you find a sweet beach house in Honolulu on Airbnb. The listing description doesn’t show how many beds are available. In the Airbnb mobile app, you ask “Does your house have enough beds to accommodate six people?”, and anxiously wait for the host to reply. However, the host is too busy to reply immediately. You get worried because you may miss out on other listings while waiting for the reply.

In another situation, you booked a summer trip with your best friend to Paris well in advance of when you plan to travel. Yet unexpectedly, just a few days before the trip, your friend tells you that you may need to change the schedule because she got injured. You are thinking of canceling the booking, but you are not sure if a full refund will be issued. You ask the host through an in-app message about the cancellation policy, and hope they can reply quickly. However, you have to wait for many hours because it is now midnight in Paris time.

We recognize these scenarios can cause anxiety and confusion, and believe there are ways to address them in a much better way. In the aforementioned two cases, answering questions in a real-time fashion is especially desirable. When inconvenient situations like these arise, Airbnb’s in-app messaging platform is a critical channel to facilitate communications. On the other hand, requiring all hosts to instantly respond to guests places lots of burden on them, not to mention that this is unrealistic.

Using recent conversational AI technologies, three Airbnb teams — the Shared Products, Applied Machine Learning, and Machine Learning Infrastructure — have developed a machine learning framework together that can mitigate the problem. The framework is capable of automatically classifying certain guest messages to help us better understand guest intent. Therefore, it can help greatly shorten the response time for guests and reduce the overall workload required for hosts. It also allows Airbnb to provide essential guidance and thus a seamless communication experience for both guests and hosts.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*rAg_GNQYzqNLzCUE)

 _Figure 1: A concept that illustrates a guest asking a host for dining recommendations nearby._

## Identifying Message Intent

Behind every message sent is an intent, be it to work out logistics, clarify details, or connect with the host. To improve upon the existing communication experience, it is vital for the AI to identify this “intent” correctly as a first step. However, this is a challenging task because it is difficult to identify the exhaustive set of intents that could exist within millions of messages.

To address this challenge, we set up our solutions in two phases: In **Phase 1** , we used a classic unsupervised approach — [Latent Dirichlet Allocation (LDA)](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) — to discover potential topics (intents) in the large message corpus. In **Phase 2** , we moved to supervised learning techniques, but used the topics derived from Phase 1 as intent labels for each message. Specifically, we built a multi-class classification model using a canonical Convolutional Neural Network (CNN) architecture. The two phases create a powerful framework for us to accurately understand the text data on our messaging platform.

### Intent Discovery

The first challenge in this problem is to discover existing topics (intents) from the enormous messaging corpus without prior knowledge. One might think of using embedding techniques to generate message-level clusters and thus topics. However a key assumption here is that only one primary topic exists in a message, which does not hold for Airbnb data. On Airbnb, people tend to set up context before they start to type core messages, and it is common to have one message containing several pieces of information that are not quite relevant to each other.

Here is an example. A guest actually wants to ask how they could store the luggage for early check-in. But they may tell the host about their arrival time first before asking the real check-in question. For humans, it is relatively easy to decompose the topics and figure out that the key topic is “early check-in possibility”. For embedding methods however, neither one single embedding vector nor algebraic aggregations of several different embedding vectors could represent the key topic. What we really need is an algorithm that can detect distinct underlying topics, and decide which one is the primary one based on probability scores.

Thus LDA becomes a natural choice for our purposes. First, LDA is a probabilistic model, which gives a probabilistic composition of topics in a message. Second, LDA assumes each word is drawn from certain word distribution that characterizes a unique topic, and each message can contain many different topics (see Figure 2 below for a graphical model representation along with the joint distribution of the variables). The word distribution allows human judgement to weigh in when deciding what each topic means.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*_hEBEBI_8605dEWzjlqueA.png)

Figure 2: A graphical model representation of LDA by [David Blei et al.](http://www.cs.columbia.edu/~blei/papers/BleiLafferty2009.pdf) along with the joint probabilities of the observed (shaded nodes) and hidden (unshaded nodes) units

Figure 3 shows a 2D visualization of the generated topics using [pyLDAvis](https://github.com/bmabey/pyLDAvis). We determined the number of topics (hyperparameter _K_) in LDA to be the one generating the highest [coherence score](http://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) on the validation set.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*5GTxk9AnRYIrSVI8wwuQpw.png)

 _Figure 3: A 2D visualization of inter-topic distances_[ _calculated based on topic-term distribution and projected via principal component analysis (PCA)_](https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf)_. The size of the circle is determined by the prevalence of the topic._

Due to time constraints, we didn’t invest much time in methods like [doc2vec](https://arxiv.org/abs/1405.4053) and [BERT](https://arxiv.org/pdf/1810.04805.pdf). Even though these methods have constraints as mentioned above, they do take the word order into account and could be attractive alternatives for intent discovery purposes. We remain open to these methods and plan to revisit them at a later time.

### **Labeling: From Unsupervised to Supervised**

Labeling is a critical component of Phase 2, as it builds up a key transition from an unsupervised solution to a supervised one. Even though a sketch of the intent space in Phase 1 has already been detected, we do not have full control of the granularity due to its unsupervised nature. This is particularly problematic if certain Airbnb product needs to address specific message intents which may not have been detected in Phase 1. It is also hard to evaluate the efficacy of LDA results for each message without a clearly predefined intent label for that message as the ground truth.

Just as intent discovery, the first challenge of labeling is to determine what labels to define. More importantly, we need to ensure that the quality of the labels is high. Our solution is to perform an iterative process that starts from the topics discovered from LDA, but leverages product feedback to generate a final set of labels. First, we _pilot labeled_ a small sample by having each message labeled by multiple people to evaluate labeling quality. We then refined the label definitions based off the [_inter-rater agreement_](https://en.wikipedia.org/wiki/Inter-rater_reliability) for each intent label, and kicked off formal labeling with a much larger data size. During the formal round, each message is reviewed once for the majority of the data. We keep a small portion of messages that are labeled by multiple reviewers so that we could _identify the limits in prediction accuracy that our model could achieve due to human-level error_. Each message is completely anonymized with Personally identifiable information (PII) scrubbed throughout the process.

In terms of labeling resource, we secured our internal product specialists who were able to provide high-quality labeling service for the message data. The labeling service turned out to be much more customizable and reliable compared with third-party vendors, and also exemplified a great collaboration between different organizations of a company.

During the labeling process, we found that about 13% of our target messages has multi-intent. **Multi-intent** is a situation where people ask questions with two or more different intents in one single message. When multi-intent occurred, we asked our specialists to assign each specific intent to the corresponding sentences. Sentences assigned with one single intent were used as an independent training sample when building the intent classification model. We demonstrate how they are handled in real-time serving in the _Productionization_ section (Figure 6).

### **Intent Classification with CNN**

Convolutional Neural Network (CNN) and Recurrent Neural Network (RNN) have been very popular methods for NLP tasks. In this work we focus on CNN due to its implementation simplicity, reported high accuracy, and especially fast speed (at both training and inference time). [Piero Molino et al., 2018](https://arxiv.org/pdf/1807.01337.pdf) showed that Word CNN performs less than 1% worse than the Char C-RNN on the same dataset and hardware, while being about 9 times faster during both training and inference. In our case, it takes us 10 minutes on average for the validation error to converge while it takes 60 minutes on average for RNN to converge to the same level. This results in a much slower model iteration and development when taking hyperparameter tuning into account.

In terms of model accuracy, [Wenpeng Yin, et al.,2017](https://arxiv.org/pdf/1702.01923.pdf) did a thorough comparison of CNN and RNN on different text classification tasks. They found that CNN actually performs better than RNN when the classification is determined by some key phrases rather than comprehending the whole long-range semantics. In our case, we usually do not need to have the full context of a guest’s message in order to identify the intent of their question. Rather, the intent is mostly determined by the key phrases such as “how many beds do you have?” or “is street parking available?”

After extensive literature review, we decided to adopt [Yoon Kim,2014](https://arxiv.org/pdf/1408.5882.pdf) and [Ye Zhang et al.,2016](https://arxiv.org/pdf/1510.03820.pdf), where a simple one-layer CNN followed by one 1-max pooling layer was proposed. Unlike the original work, we designed 4 different filter sizes each with 100 filters.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*qaPnMYBFQQQe1Aku)

 _Figure 4: Illustration of a CNN architecture for sentence classification from Ye Zhang et al._

To prepare for the embedding layer, we pre-trained word embeddings based on large out-of-sample Airbnb messaging corpus. We performed careful text preprocessing, and found that certain preprocessing steps such as tagging certain information are especially helpful in reducing noise as they normalize information like URLs, emails, date, time, phone number, etc. Below is an example of the most similar words for the word `house` generated by word2vec models trained without and with such preprocessing steps:

Most similar words for “house” generated by word2vec models trained without / with extra preprocessing steps

To be consistent, we used the same preprocessing steps throughout training word embeddings, offline training for message intent classifier, as well as online inference for real-time messages. Our to-be-open-sourced [Bighead Library](https://conferences.oreilly.com/strata/strata-ny-2018/public/schedule/detail/69383) made all these feasible.

## Get Michelle (Guqian) Du’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

The overall accuracy of the Phase-1&2 solution is around 70% and outperforms the Phase-1 only solution by a magnitude of 50–100%. It also exceeds the accuracy of predicting based on label distribution by a magnitude of ~400%.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*F1i8MJzWS_Q3jkQi9GA2pw.png)

 _Table 1: Comparison on overall accuracy between Phase-1 &2, Phase-1 Only, and Predict by Label Distribution. Pre-trip: before a trip starts. On-trip: during a trip._

We evaluated classification accuracies class by class, especially when the dataset was imbalanced across different classes. Figure 5 is the confusion matrix for the on-trip model mentioned above. We masked the actual category name with `category_1` , `category_2`, etc. due to confidentiality. As one may see, a clear diagonal pattern can be found, which means the majority of the class predictions matches the ground truth.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*z2jbIjtjuC2cf3qd)

 _Figure 5: The normalized confusion matrix for the on-trip model results_

Table 2 shows some example categories that are well predicted. In these categories, the key phrases are strong indicators of message intent that the CNN model captures very well.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*oM1eKz6ZNT8-vCxngpxeJQ.png)

Table 2: Example categories that are well predicted

Table 3 below shows some example categories that are not well predicted.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*_Q_zVIHggtoUTQ2n05B1VQ.png)

Table 3: Example categories that are not so well predicted

There were two primary root causes for the misclassifications:

1\. Human errors in labeling. For example, some labelers mistakenly think that “Do you have recommendations on hiking or boat tours?” is a general question, but this type of questions are considered specific questions in our categories.

2\. Label ambiguity. For example, “Could you recommend some things to do in the area? We were looking to go to a public beach or lake”, can be labeled as a generic question because the first sentence, “Could you recommend some things to do in the area?”, is a general ask. However the next sentence in the same message, “We were looking to go to a public beach or lake”, apparently has very specific intent. The message does not neatly fit into either label (specific or generic) as a whole.

## **Productionization — Online Serving**

We productionized our framework using [Bighead](https://conferences.oreilly.com/strata/strata-ny-2018/public/schedule/detail/69383), a comprehensive ML infrastructure tool developed by the ML Infrastructure Team at Airbnb. The models are served through Deep Thought, the online inference component of Bighead. There will be a separate blog post introducing Bighead in more details — stay tuned!

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*ZXJykjU62lCovpyr)

 _Figure 6: The offline training & online serving workflow of Phase II._

## **Applications**

Here is a glimpse of some of the applications that are either happening or are being planned for the near future.

  * Predicting customer support issues leveraging message intent history
  * Guiding through cancellation / payment / refund process by identifying such intents early
  * Improving booking experience by identifying guest concerns
  * Providing instant smart response by identifying guest / host needs

## **Conclusion**

We have developed a framework for message intent understanding that evolved from intent discovery to intent classification using unsupervised and supervised learning techniques. The work empowers a variety of product applications that facilitate a seamless communication experience through Airbnb’s messaging platform. Below are a few takeaways:

  * Unsupervised learning can be a powerful tool to provide labels for a supervised learning solution.
  * Text preprocessing could play a critical role when training word embeddings using customized text corpus.
  * Label quality is the key to model performance. Figuring out the right ways to reduce human error in the labeling process could have tremendous impact on your model accuracy if the bottleneck is label accuracy in your problem in the first place.

Up next, we plan to further improve our solution from several aspects:

  * Improve unsupervised learning results for intent discovery by experimenting with more language representation models such as doc2vec, BERT
  * Improve labeling efficiency through enhanced labeling tools with semi-supervised learning
  * Improve labeling quality with more rigorous definitions and professional training
  * Explore hosts’ intents beyond those of the guests

As we deepen our understanding of Airbnb’s text data, we are constantly identifying new areas where we can leverage this technology to improve the Airbnb product. We also plan to support other languages to assist our communities worldwide.

## Acknowledgement

This work is in collaboration with _John Park_ and [_Sam Shadwell_](/@samshadwell). We would also like to thank [_Joy Zhang_](/@joycmu/) _, Peter Gannon_ , [_Patrick Srail_](/@patricksrail) _,_[_Junshuo Liao_](/@junshuoliao) _, Andrew Hoh,_[_Darrick Brown_](/@darrick.brown) _, Atul Kale,_[_Jeff Feng_](/@jtfeng) _, Peggy Shao_ , [_Cindy Chen_](/@Magic_Cindy) _, Wei Han, Alfredo Luque_ , [_Roy Stanfield,_](/@RoyStanfield)[_Joshua Pekera_](/@joshuapekera) for their support and feedback throughout this project! We’d also like to thank [_Xiaohan Zeng_](/@XiaohanZeng) _, Dai Li,_ and _Rebecca Rosenfelt_ for their kind help in proofreading!

Airbnb is always seeking outstanding people to join our team! If you are interested in working on problems such as the one in this post, please check out our [open positions in Data Science and Analytics](https://www.airbnb.com/careers/departments/data-science-analytics), and send your application!

[Machine Learning](/tag/machine-learning?source=post_page-----6a55f5400a0c---------------------------------------)

[NLP](/tag/nlp?source=post_page-----6a55f5400a0c---------------------------------------)

[Data Science](/tag/data-science?source=post_page-----6a55f5400a0c---------------------------------------)

[AI](/tag/ai?source=post_page-----6a55f5400a0c---------------------------------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F6a55f5400a0c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&user=Michelle+%28Guqian%29+Du&userId=f81a16adf62&source=---footer_actions--6a55f5400a0c---------------------clap_footer------------------)

1.2K

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2F6a55f5400a0c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&user=Michelle+%28Guqian%29+Du&userId=f81a16adf62&source=---footer_actions--6a55f5400a0c---------------------clap_footer------------------)

1.2K

6

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F6a55f5400a0c&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&source=---footer_actions--6a55f5400a0c---------------------bookmark_footer------------------)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:48:48/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--6a55f5400a0c---------------------------------------)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:64:64/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--6a55f5400a0c---------------------------------------)

Follow

## [Published in The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---post_publication_info--6a55f5400a0c---------------------------------------)

[156K followers](/airbnb-engineering/followers?source=post_page---post_publication_info--6a55f5400a0c---------------------------------------)

·[Last published 4 days ago](/airbnb-engineering/my-journey-to-airbnb-anna-sulkina-85216183d094?source=post_page---post_publication_info--6a55f5400a0c---------------------------------------)

Creative engineers and data scientists building a world where you can belong anywhere. <http://airbnb.io>

Follow

[![Michelle \(Guqian\) Du](https://miro.medium.com/v2/resize:fill:48:48/1*ttzEe83XytaRWhbtABdcFA.jpeg)](/@michelle.du?source=post_page---post_author_info--6a55f5400a0c---------------------------------------)

[![Michelle \(Guqian\) Du](https://miro.medium.com/v2/resize:fill:64:64/1*ttzEe83XytaRWhbtABdcFA.jpeg)](/@michelle.du?source=post_page---post_author_info--6a55f5400a0c---------------------------------------)

Follow

## [Written by Michelle (Guqian) Du](/@michelle.du?source=post_page---post_author_info--6a55f5400a0c---------------------------------------)

[194 followers](/@michelle.du/followers?source=post_page---post_author_info--6a55f5400a0c---------------------------------------)

·[8 following](/@michelle.du/following?source=post_page---post_author_info--6a55f5400a0c---------------------------------------)

Data Science & Machine Learning @ Airbnb

Follow

## Responses (6)

[](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page---post_responses--6a55f5400a0c---------------------------------------)

![](https://miro.medium.com/v2/resize:fill:32:32/1*dmbNkD5D-u45r44go_cf0g.png)

Write a response

[What are your thoughts?](/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fdiscovering-and-classifying-in-app-message-intent-at-airbnb-6a55f5400a0c&source=---post_responses--6a55f5400a0c---------------------respond_sidebar------------------)

Cancel

Respond

[![Guilherme Peixoto](https://miro.medium.com/v2/resize:fill:32:32/2*q14hZxq36OTZPcxFbuE8Jg.png)](/@gpalmape?source=post_page---post_responses--6a55f5400a0c----0-----------------------------------)

[Guilherme Peixoto](/@gpalmape?source=post_page---post_responses--6a55f5400a0c----0-----------------------------------)

[Feb 6, 2019](/@gpalmape/excellent-post-per-usual-thank-you-for-sharing-your-findings-8edbcf504757?source=post_page---post_responses--6a55f5400a0c----0-----------------------------------)
    
    
    Excellent post! Per usual, thank you for sharing your findings.
    
    A couple of questions — regarding the dataset imbalance, did you perform any particular strategy (under/over sampling) or strong regularization proved to be enough?
    
    Also, please correct…more

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F8edbcf504757&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40gpalmape%2Fexcellent-post-per-usual-thank-you-for-sharing-your-findings-8edbcf504757&user=Guilherme+Peixoto&userId=9effaab8957e&source=---post_responses--8edbcf504757----0-----------------respond_sidebar------------------)

5

1 reply

Reply

[![Jaskeerat Bedi](https://miro.medium.com/v2/resize:fill:32:32/0*xdFGLi8widd5VUO1.)](/@bedi.jaskeerat?source=post_page---post_responses--6a55f5400a0c----1-----------------------------------)

[Jaskeerat Bedi](/@bedi.jaskeerat?source=post_page---post_responses--6a55f5400a0c----1-----------------------------------)

[Jan 31, 2019](/@bedi.jaskeerat/thoroughly-enjoyed-reading-390e6315ff47?source=post_page---post_responses--6a55f5400a0c----1-----------------------------------)
    
    
    Thoroughly enjoyed reading! Bravo on doing a great job of context setting especially starting with a legit user need and supporting it with a detailed ML framework.

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2F390e6315ff47&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40bedi.jaskeerat%2Fthoroughly-enjoyed-reading-390e6315ff47&user=Jaskeerat+Bedi&userId=10602f5618ec&source=---post_responses--390e6315ff47----1-----------------respond_sidebar------------------)

1

Reply

[![Noah Chasek-Macfoy](https://miro.medium.com/v2/resize:fill:32:32/2*E4TE5eiqoG1fYgydcRPkpg.jpeg)](/@bantucaravan?source=post_page---post_responses--6a55f5400a0c----2-----------------------------------)

[Noah Chasek-Macfoy](/@bantucaravan?source=post_page---post_responses--6a55f5400a0c----2-----------------------------------)

[Dec 13, 2019](/@bantucaravan/great-article-cde545b5140a?source=post_page---post_responses--6a55f5400a0c----2-----------------------------------)
    
    
    Great Article! How necessary was the unsupervised step? Did you only use intent categories identified by LDA? Did the LDA grouping speed up the manual labeling process? Did you ever determine whether a supervised intent model would have been…more

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fp%2Fcde545b5140a&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40bantucaravan%2Fgreat-article-cde545b5140a&user=Noah+Chasek-Macfoy&userId=c79239e620cd&source=---post_responses--cde545b5140a----2-----------------respond_sidebar------------------)

Reply

See all responses

## More from Michelle (Guqian) Du and The Airbnb Tech Blog

![Empowering Data Science with Engineering Education](https://miro.medium.com/v2/resize:fit:679/format:webp/1*PytoZY4m9iTzDuIdiWMHTg.jpeg)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----0---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----0---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

by

[Michelle (Guqian) Du](/@michelle.du?source=post_page---author_recirc--6a55f5400a0c----0---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

## [Empowering Data Science with Engineering EducationEngineering education enables data scientists to better interface with engineering and ensures higher data quality.](/airbnb-engineering/empowering-data-science-with-data-engineering-education-ef2acabd3042?source=post_page---author_recirc--6a55f5400a0c----0---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

Jan 18, 2019

[A clap icon560A response icon4](/airbnb-engineering/empowering-data-science-with-data-engineering-education-ef2acabd3042?source=post_page---author_recirc--6a55f5400a0c----0---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fef2acabd3042&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fempowering-data-science-with-data-engineering-education-ef2acabd3042&source=---author_recirc--6a55f5400a0c----0-----------------bookmark_preview----e7065724_1609_4987_b8f9_218046d9784f--------------)

![A Deep Dive into Airbnb’s Server-Driven UI System](https://miro.medium.com/v2/resize:fit:679/format:webp/0*CedYKpSYMIGEiX7m)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----1---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----1---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

by

[Ryan Brooks](/@rbro112?source=post_page---author_recirc--6a55f5400a0c----1---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

## [A Deep Dive into Airbnb’s Server-Driven UI SystemHow Airbnb ships features faster across web, iOS, and Android using a server-driven UI system named Ghost Platform 👻.](/airbnb-engineering/a-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5?source=post_page---author_recirc--6a55f5400a0c----1---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

Jun 29, 2021

[A clap icon4.3KA response icon40](/airbnb-engineering/a-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5?source=post_page---author_recirc--6a55f5400a0c----1---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F842244c5f5&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fa-deep-dive-into-airbnbs-server-driven-ui-system-842244c5f5&source=---author_recirc--6a55f5400a0c----1-----------------bookmark_preview----e7065724_1609_4987_b8f9_218046d9784f--------------)

![Pay As a Local](https://miro.medium.com/v2/resize:fit:679/format:webp/1*6K6D4WxFwqlwdtBc6uzczw.jpeg)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----2---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----2---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

by

[Gerum Haile](/@gerum.haile?source=post_page---author_recirc--6a55f5400a0c----2---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

## [Pay As a LocalHow Airbnb rolled out 20+ locally relevant payment methods worldwide in just 14 months](/airbnb-engineering/pay-as-a-local-bef469b72f32?source=post_page---author_recirc--6a55f5400a0c----2---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

Jan 12

[A clap icon82A response icon1](/airbnb-engineering/pay-as-a-local-bef469b72f32?source=post_page---author_recirc--6a55f5400a0c----2---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fbef469b72f32&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fpay-as-a-local-bef469b72f32&source=---author_recirc--6a55f5400a0c----2-----------------bookmark_preview----e7065724_1609_4987_b8f9_218046d9784f--------------)

![How Airbnb Achieved Metric Consistency at Scale](https://miro.medium.com/v2/resize:fit:679/format:webp/1*rB53PQsJi73IeA-eIeucIg.png)

[![The Airbnb Tech Blog](https://miro.medium.com/v2/resize:fill:20:20/1*_eS85njIKe8OI-SnQ7OLRQ.png)](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----3---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

In

[The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c----3---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

by

[Robert Chang](/@rchang?source=post_page---author_recirc--6a55f5400a0c----3---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

## [How Airbnb Achieved Metric Consistency at ScalePart-I: Introducing Minerva — Airbnb’s Metric Platform](/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70?source=post_page---author_recirc--6a55f5400a0c----3---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

Apr 30, 2021

[A clap icon2.2KA response icon10](/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70?source=post_page---author_recirc--6a55f5400a0c----3---------------------e7065724_1609_4987_b8f9_218046d9784f--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ff23cc53dea70&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fhow-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70&source=---author_recirc--6a55f5400a0c----3-----------------bookmark_preview----e7065724_1609_4987_b8f9_218046d9784f--------------)

[See all from Michelle (Guqian) Du](/@michelle.du?source=post_page---author_recirc--6a55f5400a0c---------------------------------------)

[See all from The Airbnb Tech Blog](https://medium.com/airbnb-engineering?source=post_page---author_recirc--6a55f5400a0c---------------------------------------)

## Recommended from Medium

![The AI Bubble Is About To Burst, But The Next Bubble Is Already Growing](https://miro.medium.com/v2/resize:fit:679/format:webp/0*jQ7Z0Y2Rw8kblsEX)

[![Will Lockett](https://miro.medium.com/v2/resize:fill:20:20/1*V0qWMQ8V5_NaF9yUoHAdyg.jpeg)](/@wlockett?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[Will Lockett](/@wlockett?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

## [The AI Bubble Is About To Burst, But The Next Bubble Is Already GrowingTechbros are preparing their latest bandwagon.](/@wlockett/the-ai-bubble-is-about-to-burst-but-the-next-bubble-is-already-growing-383c0c0c7ede?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

Sep 14, 2025

[A clap icon22KA response icon951](/@wlockett/the-ai-bubble-is-about-to-burst-but-the-next-bubble-is-already-growing-383c0c0c7ede?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F383c0c0c7ede&operation=register&redirect=https%3A%2F%2Fwlockett.medium.com%2Fthe-ai-bubble-is-about-to-burst-but-the-next-bubble-is-already-growing-383c0c0c7ede&source=---read_next_recirc--6a55f5400a0c----0-----------------bookmark_preview----ce480f77_36a7_4d26_ad57_68e4766430db--------------)

![Stanford Just Killed Prompt Engineering With 8 Words \(And I Can’t Believe It Worked\)](https://miro.medium.com/v2/resize:fit:679/format:webp/1*va3sFwIm26snbj5ly9ZsgA.jpeg)

[![Generative AI](https://miro.medium.com/v2/resize:fill:20:20/1*M4RBhIRaSSZB7lXfrGlatA.png)](https://medium.com/generative-ai?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

In

[Generative AI](https://medium.com/generative-ai?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

by

[Adham Khaled](/@adham__khaled__?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

## [Stanford Just Killed Prompt Engineering With 8 Words (And I Can’t Believe It Worked)ChatGPT keeps giving you the same boring response? This new technique unlocks 2× more creativity from ANY AI model — no training required…](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

Oct 19, 2025

[A clap icon23KA response icon618](/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F8349d6524d2b&operation=register&redirect=https%3A%2F%2Fgenerativeai.pub%2Fstanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b&source=---read_next_recirc--6a55f5400a0c----1-----------------bookmark_preview----ce480f77_36a7_4d26_ad57_68e4766430db--------------)

![I Stopped Using ChatGPT for 30 Days. What Happened to My Brain Was Terrifying.](https://miro.medium.com/v2/resize:fit:679/format:webp/1*z4UOJs0b33M4UJXq5MXkww.png)

[![Level Up Coding](https://miro.medium.com/v2/resize:fill:20:20/1*5D9oYBd58pyjMkV_5-zXXQ.jpeg)](https://medium.com/gitconnected?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

In

[Level Up Coding](https://medium.com/gitconnected?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

by

[Teja Kusireddy](/@teja.kusireddy23?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

## [I Stopped Using ChatGPT for 30 Days. What Happened to My Brain Was Terrifying.91% of you will abandon 2026 resolutions by January 10th. Here’s how to be in the 9% who actually win.](/gitconnected/i-stopped-using-chatgpt-for-30-days-what-happened-to-my-brain-was-terrifying-70d2a62246c0?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

Dec 28, 2025

[A clap icon5.5KA response icon220](/gitconnected/i-stopped-using-chatgpt-for-30-days-what-happened-to-my-brain-was-terrifying-70d2a62246c0?source=post_page---read_next_recirc--6a55f5400a0c----0---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F70d2a62246c0&operation=register&redirect=https%3A%2F%2Flevelup.gitconnected.com%2Fi-stopped-using-chatgpt-for-30-days-what-happened-to-my-brain-was-terrifying-70d2a62246c0&source=---read_next_recirc--6a55f5400a0c----0-----------------bookmark_preview----ce480f77_36a7_4d26_ad57_68e4766430db--------------)

![6 brain images](https://miro.medium.com/v2/resize:fit:679/format:webp/1*Q-mzQNzJSVYkVGgsmHVjfw.png)

[![Write A Catalyst](https://miro.medium.com/v2/resize:fill:20:20/1*KCHN5TM3Ga2PqZHA4hNbaw.png)](https://medium.com/write-a-catalyst?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

In

[Write A Catalyst](https://medium.com/write-a-catalyst?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

by

[Dr. Patricia Schmidt](/@creatorschmidt?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

## [As a Neuroscientist, I Quit These 5 Morning Habits That Destroy Your BrainMost people do #1 within 10 minutes of waking (and it sabotages your entire day)](/write-a-catalyst/as-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

Jan 14

[A clap icon29KA response icon500](/write-a-catalyst/as-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226?source=post_page---read_next_recirc--6a55f5400a0c----1---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F3efe1f410226&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fwrite-a-catalyst%2Fas-a-neuroscientist-i-quit-these-5-morning-habits-that-destroy-your-brain-3efe1f410226&source=---read_next_recirc--6a55f5400a0c----1-----------------bookmark_preview----ce480f77_36a7_4d26_ad57_68e4766430db--------------)

![An example of a perfect, human designed dashboard interface for desktop and mobile phone](https://miro.medium.com/v2/resize:fit:679/format:webp/1*C8RVDKs_uZrVUdgpsF6Fmw.png)

[![Michal Malewicz](https://miro.medium.com/v2/resize:fill:20:20/1*149zXrb2FXvS_mctL4NKSg.png)](/@michalmalewicz?source=post_page---read_next_recirc--6a55f5400a0c----2---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[Michal Malewicz](/@michalmalewicz?source=post_page---read_next_recirc--6a55f5400a0c----2---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

## [The End of Dashboards and Design SystemsDesign is becoming quietly human again.](/@michalmalewicz/the-end-of-dashboards-and-design-systems-5d98ec9de627?source=post_page---read_next_recirc--6a55f5400a0c----2---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

Nov 26, 2025

[A clap icon5.6KA response icon212](/@michalmalewicz/the-end-of-dashboards-and-design-systems-5d98ec9de627?source=post_page---read_next_recirc--6a55f5400a0c----2---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F5d98ec9de627&operation=register&redirect=https%3A%2F%2Fmichalmalewicz.medium.com%2Fthe-end-of-dashboards-and-design-systems-5d98ec9de627&source=---read_next_recirc--6a55f5400a0c----2-----------------bookmark_preview----ce480f77_36a7_4d26_ad57_68e4766430db--------------)

![Stop Memorizing Design Patterns: Use This Decision Tree Instead](https://miro.medium.com/v2/resize:fit:679/format:webp/1*xfboC-sVIT2hzWkgQZT_7w.png)

[![Women in Technology](https://miro.medium.com/v2/resize:fill:20:20/1*kd0DvPkLdn59Emtg_rnsqg.png)](https://medium.com/womenintechnology?source=post_page---read_next_recirc--6a55f5400a0c----3---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

In

[Women in Technology](https://medium.com/womenintechnology?source=post_page---read_next_recirc--6a55f5400a0c----3---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

by

[Alina Kovtun✨](/@akovtun?source=post_page---read_next_recirc--6a55f5400a0c----3---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

## [Stop Memorizing Design Patterns: Use This Decision Tree InsteadChoose design patterns based on pain points: apply the right pattern with minimal over-engineering in any OO language.](/womenintechnology/stop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa?source=post_page---read_next_recirc--6a55f5400a0c----3---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

Jan 29

[A clap icon3.1KA response icon26](/womenintechnology/stop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa?source=post_page---read_next_recirc--6a55f5400a0c----3---------------------ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fe84f22fca9fa&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fwomenintechnology%2Fstop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa&source=---read_next_recirc--6a55f5400a0c----3-----------------bookmark_preview----ce480f77_36a7_4d26_ad57_68e4766430db--------------)

[See more recommendations](/?source=post_page---read_next_recirc--6a55f5400a0c---------------------------------------)

[Help](https://help.medium.com/hc/en-us?source=post_page-----6a55f5400a0c---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----6a55f5400a0c---------------------------------------)

[About](/about?autoplay=1&source=post_page-----6a55f5400a0c---------------------------------------)

[Careers](/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----6a55f5400a0c---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----6a55f5400a0c---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----6a55f5400a0c---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----6a55f5400a0c---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----6a55f5400a0c---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----6a55f5400a0c---------------------------------------)

![Michelle \(Guqian\) Du's profile picture](https://miro.medium.com/v2/resize:fill:48:48/1*ttzEe83XytaRWhbtABdcFA.jpeg)

## Be the first to hear about new stories from Michelle (Guqian) Du

#### Join Medium for free to get updates from Michelle (Guqian) Du sent right to your inbox.

Your email

Create account

Other sign up options

Already have an account? Sign in

By clicking "Create Account", you accept Medium's [Terms of Service](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=register-----6a55f5400a0c-----------------f81a16adf62----subscribe_to_author------------------) and [Privacy Policy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=register-----6a55f5400a0c-----------------f81a16adf62----subscribe_to_author------------------).

This site uses reCaptcha and the Google [Privacy Policy](https://policies.google.com/privacy?source=register-----6a55f5400a0c-----------------f81a16adf62----subscribe_to_author------------------) and [Terms of Service](https://policies.google.com/terms?source=register-----6a55f5400a0c-----------------f81a16adf62----subscribe_to_author------------------) apply.