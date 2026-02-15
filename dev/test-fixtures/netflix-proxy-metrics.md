# Source: https://netflixtechblog.com/improve-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac

[Sitemap](/sitemap/sitemap.xml)

[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fnetflixtechblog.com%2Fimprove-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

[Medium Logo](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

[Write](https://medium.com/m/signin?operation=register&redirect=https%3A%2F%2Fmedium.com%2Fnew-story&source=---top_nav_layout_nav-----------------------new_post_topnav------------------)

[Search](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

Sign up

[Sign in](https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fnetflixtechblog.com%2Fimprove-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac&source=post_page---top_nav_layout_nav-----------------------global_nav------------------)

![](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

## [Netflix TechBlog](https://netflixtechblog.com/?source=post_page---publication_nav-2615bd06b42e-64c786c2a3ac---------------------------------------)

·

Follow publication

[![Netflix TechBlog](https://miro.medium.com/v2/resize:fill:76:76/1*ty4NvNrGg4ReETxqU2N3Og.png)](https://netflixtechblog.com/?source=post_page---post_publication_sidebar-2615bd06b42e-64c786c2a3ac---------------------------------------)

Learn about Netflix’s world class engineering efforts, company culture, product developments and more.

Follow publication

# **Improve Your Next Experiment by Learning Better Proxy Metrics From Past Experiments**

[![Netflix Technology Blog](https://miro.medium.com/v2/resize:fill:64:64/1*BJWRqfSMf9Da9vsXG9EBRQ.jpeg)](https://netflixtechblog.medium.com/?source=post_page---byline--64c786c2a3ac---------------------------------------)

[Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page---byline--64c786c2a3ac---------------------------------------)

6 min read

·

Aug 26, 2024

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fnetflix-techblog%2F64c786c2a3ac&operation=register&redirect=https%3A%2F%2Fnetflixtechblog.com%2Fimprove-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac&user=Netflix+Technology+Blog&userId=c3aeaf49d8a4&source=---header_actions--64c786c2a3ac---------------------clap_footer------------------)

\--

4

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F64c786c2a3ac&operation=register&redirect=https%3A%2F%2Fnetflixtechblog.com%2Fimprove-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac&source=---header_actions--64c786c2a3ac---------------------bookmark_footer------------------)

Listen

Share

 _By_[ _Aurélien Bibaut_](https://www.linkedin.com/in/aurelien-bibaut/) _,_[_Winston Chou_](https://www.linkedin.com/in/winston-chou-6491b0168/) _,_[_Simon Ejdemyr_](https://www.linkedin.com/in/simon-ejdemyr-22b920123/) _, and_[ _Nathan Kallus_](https://www.linkedin.com/in/kallus/)

Press enter or click to view image in full size

We are excited to share [our work](https://arxiv.org/pdf/2402.17637) on how to learn good proxy metrics from historical experiments at [KDD 2024](https://kdd2024.kdd.org/). This work addresses a fundamental question for technology companies and academic researchers alike: how do we establish that a treatment that improves short-term (statistically sensitive) outcomes also improves long-term (statistically insensitive) outcomes? Or, faced with multiple short-term outcomes, how do we optimally trade them off for long-term benefit?

For example, in an A/B test, you may observe that a product change improves the click-through rate. However, the test does not provide enough signal to measure a change in long-term retention, leaving you in the dark as to whether this treatment makes users more satisfied with your service. The click-through rate is a _proxy metric_ (_S_ , for surrogate, in our paper) while retention is a downstream _business outcome_ or _north star metric_(_Y_). We may even have several proxy metrics, such as other types of clicks or the length of engagement after click. Taken together, these form a _vector_ of proxy metrics.

The goal of our work is to understand the true relationship between the proxy metric(s) and the north star metric — so that we can assess a proxy’s ability to stand in for the north star metric, learn how to combine multiple metrics into a single best one, and better explore and compare different proxies.

## Get Netflix Technology Blog’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Several intuitive approaches to understanding this relationship have surprising pitfalls:

  * **Looking only at user-level correlations between the proxy _S_ and north star _Y_.** Continuing the example from above, you may find that users with a higher click-through rate also tend to have a higher retention. But this does not mean that a _product change_ that improves the click-through rate will also improve retention (in fact, promoting clickbait may have the opposite effect). This is because, as any introductory causal inference class will tell you, there are many confounders between _S_ and _Y_ — many of which you can never reliably observe and control for.
  * **Looking naively at treatment effect correlations between _S_ and _Y._** Suppose you are lucky enough to have many historical A/B tests. Further imagine the ordinary least squares (OLS) regression line through a scatter plot of _Y_ on _S_ in which each point represents the (_S_ ,_Y_)-treatment effect from a previous test. Even if you find that this line has a positive slope, you unfortunately _cannot_ conclude that product changes that improve _S_ will also improve _Y_. The reason for this is correlated measurement error — if _S_ and _Y_ are positively correlated in the population, then treatment arms that happen to have more users with high _S_ will also have more users with high _Y_.

Between these naive approaches, we find that the second one is the easier trap to fall into. This is because the dangers of the first approach are well-known, whereas covariances between _estimated_ treatment effects can appear misleadingly causal. In reality, these covariances can be severely biased compared to what we actually care about: covariances between _true_ treatment effects. In the extreme — such as when the negative effects of clickbait are substantial but clickiness and retention are highly correlated at the user level — the true relationship between _S_ and _Y_ can be negative even if the OLS slope is positive. Only more data per experiment could diminish this bias — using more experiments as data points will only yield more precise estimates of the badly biased slope. At first glance, this would appear to imperil any hope of using existing experiments to detect the relationship.

Press enter or click to view image in full size

 _This figure shows a hypothetical treatment effect covariance matrix between S and Y (white line; negative correlation), a unit-level sampling covariance matrix creating correlated measurement errors between these metrics (black line; positive correlation), and the covariance matrix of estimated treatment effects which is a weighted combination of the first two (orange line; no correlation)._

To overcome this bias, we propose better ways to leverage historical experiments, inspired by techniques from the literature on weak instrumental variables. More specifically, we show that three estimators are consistent for the true proxy/north-star relationship under different constraints (the [paper](https://arxiv.org/pdf/2402.17637) provides more details and should be helpful for practitioners interested in choosing the best estimator for their setting):

  * A **Total Covariance (TC)** estimator allows us to estimate the OLS slope from a scatter plot of _true_ treatment effects by subtracting the scaled measurement error covariance from the covariance of estimated treatment effects. Under the assumption that the correlated measurement error is the same across experiments (homogeneous covariances), the bias of this estimator is inversely proportional to the total number of units across all experiments, as opposed to the number of members per experiment.
  * **Jackknife Instrumental Variables Estimation (JIVE)** converges to the same OLS slope as the TC estimator but does not require the assumption of homogeneous covariances. JIVE eliminates correlated measurement error by removing each observation’s data from the computation of its instrumented surrogate values.
  * A **Limited Information Maximum Likelihood (LIML)** estimator is statistically efficient as long as there are no direct effects between the treatment and _Y_ (that is, _S_ fully mediates all treatment effects on _Y_). We find that LIML is highly sensitive to this assumption and recommend TC or JIVE for most applications.

Our methods yield linear structural models of treatment effects that are easy to interpret. As such, they are well-suited to the decentralized and rapidly-evolving practice of experimentation at Netflix, which runs [thousands of experiments per year](/experimentation-is-a-major-focus-of-data-science-across-netflix-f67923f8e985) on many diverse parts of the business. Each area of experimentation is staffed by independent Data Science and Engineering teams. While every team ultimately cares about the same north star metrics (e.g., long-term revenue), it is highly impractical for most teams to measure these in short-term A/B tests. Therefore, each has also developed proxies that are more sensitive and directly relevant to their work (e.g., user engagement or latency). To complicate matters more, teams are constantly innovating on these secondary metrics to find the right balance of sensitivity and long-term impact.

In this decentralized environment, linear models of treatment effects are a highly useful tool for coordinating efforts around proxy metrics and aligning them towards the north star:

  1. **Managing metric tradeoffs.** Because experiments in one area can affect metrics in another area, there is a need to measure all secondary metrics in all tests, but also to understand the relative impact of these metrics on the north star. This is so we can inform decision-making when one metric trades off against another metric.
  2. **Informing metrics innovation.** To minimize wasted effort on metric development, it is also important to understand how metrics correlate with the north star “net of” existing metrics.
  3. **Enabling teams to work independently.** Lastly, teams need simple tools in order to iterate on their own metrics. Teams may come up with dozens of variations of secondary metrics, and slow, complicated tools for evaluating these variations are unlikely to be adopted. Conversely, our models are easy and fast to fit, and are actively used to develop proxy metrics at Netflix.

We are thrilled about the research and implementation of these methods at Netflix — while also continuing to strive for **_great and always better_** , per our [culture](https://jobs.netflix.com/culture). For example, we still have some way to go to develop a more flexible data architecture to streamline the application of these methods within Netflix. Interested in helping us? See our [open job postings](https://jobs.netflix.com/)!

_For feedback on this blog post and for supporting and making this work better, we thank Apoorva Lal, Martin Tingley, Patric Glynn, Richard McDowell, Travis Brooks, and Ayal Chen-Zion._

[ Experimentation](https://medium.com/tag/experimentation?source=post_page-----64c786c2a3ac---------------------------------------)

[A B Testing](https://medium.com/tag/a-b-testing?source=post_page-----64c786c2a3ac---------------------------------------)

[Data Science](https://medium.com/tag/data-science?source=post_page-----64c786c2a3ac---------------------------------------)

[Machine Learning](https://medium.com/tag/machine-learning?source=post_page-----64c786c2a3ac---------------------------------------)

[Statistics](https://medium.com/tag/statistics?source=post_page-----64c786c2a3ac---------------------------------------)

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fnetflix-techblog%2F64c786c2a3ac&operation=register&redirect=https%3A%2F%2Fnetflixtechblog.com%2Fimprove-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac&user=Netflix+Technology+Blog&userId=c3aeaf49d8a4&source=---footer_actions--64c786c2a3ac---------------------clap_footer------------------)

\--

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fnetflix-techblog%2F64c786c2a3ac&operation=register&redirect=https%3A%2F%2Fnetflixtechblog.com%2Fimprove-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac&user=Netflix+Technology+Blog&userId=c3aeaf49d8a4&source=---footer_actions--64c786c2a3ac---------------------clap_footer------------------)

\--

4

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F64c786c2a3ac&operation=register&redirect=https%3A%2F%2Fnetflixtechblog.com%2Fimprove-your-next-experiment-by-learning-better-proxy-metrics-from-past-experiments-64c786c2a3ac&source=---footer_actions--64c786c2a3ac---------------------bookmark_footer------------------)

[![Netflix TechBlog](https://miro.medium.com/v2/resize:fill:96:96/1*ty4NvNrGg4ReETxqU2N3Og.png)](https://netflixtechblog.com/?source=post_page---post_publication_info--64c786c2a3ac---------------------------------------)

[![Netflix TechBlog](https://miro.medium.com/v2/resize:fill:128:128/1*ty4NvNrGg4ReETxqU2N3Og.png)](https://netflixtechblog.com/?source=post_page---post_publication_info--64c786c2a3ac---------------------------------------)

Follow

## [Published in Netflix TechBlog](https://netflixtechblog.com/?source=post_page---post_publication_info--64c786c2a3ac---------------------------------------)

[180K followers](/followers?source=post_page---post_publication_info--64c786c2a3ac---------------------------------------)

·[Last published 2 days ago](/scaling-llm-post-training-at-netflix-0046f8790194?source=post_page---post_publication_info--64c786c2a3ac---------------------------------------)

Learn about Netflix’s world class engineering efforts, company culture, product developments and more.

Follow

[![Netflix Technology Blog](https://miro.medium.com/v2/resize:fill:96:96/1*BJWRqfSMf9Da9vsXG9EBRQ.jpeg)](https://netflixtechblog.medium.com/?source=post_page---post_author_info--64c786c2a3ac---------------------------------------)

[![Netflix Technology Blog](https://miro.medium.com/v2/resize:fill:128:128/1*BJWRqfSMf9Da9vsXG9EBRQ.jpeg)](https://netflixtechblog.medium.com/?source=post_page---post_author_info--64c786c2a3ac---------------------------------------)

## [Written by Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page---post_author_info--64c786c2a3ac---------------------------------------)

[449K followers](https://netflixtechblog.medium.com/followers?source=post_page---post_author_info--64c786c2a3ac---------------------------------------)

·[1 following](https://medium.com/@netflixtechblog/following?source=post_page---post_author_info--64c786c2a3ac---------------------------------------)

Learn more about how Netflix designs, builds, and operates our systems and engineering organizations

## Responses (4)

[](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page---post_responses--64c786c2a3ac---------------------------------------)

See all responses

[Help](https://help.medium.com/hc/en-us?source=post_page-----64c786c2a3ac---------------------------------------)

[Status](https://status.medium.com/?source=post_page-----64c786c2a3ac---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=post_page-----64c786c2a3ac---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=post_page-----64c786c2a3ac---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=post_page-----64c786c2a3ac---------------------------------------)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=post_page-----64c786c2a3ac---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=post_page-----64c786c2a3ac---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=post_page-----64c786c2a3ac---------------------------------------)

[Text to speech](https://speechify.com/medium?source=post_page-----64c786c2a3ac---------------------------------------)