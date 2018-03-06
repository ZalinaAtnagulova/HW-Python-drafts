#https://agricolamz.github.io/2018_data_analysis_for_linguists/5_PCA.html#9_%D1%81%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5_pca_%D0%B8_lda

```{r}

library(tidyverse)
library(bootstrap)
library(mosaic)
wodehouse <- read_csv('https://raw.githubusercontent.com/agricolamz/2018_data_analysis_for_linguists/master/data/students/ZalinaAtnagulova/hw3_binomial_ci/hw3_wodehouse.csv')

#chapter — номер главы
#linenumber — номер абзаца в тексте
#word — слово из текста. Слова в строках идут по порядку, так же как они идут в тексте.

### 1.1
#Посчитайте среднее употребление слова “сэр” по каждой главе, 
#а потом посчитайте grand mean. Ответ выведите в формате тиббл
  
wodehouse %>% 
  count(chapter) ->
  chapter_words

wodehouse %>% 
  count(chapter, word) ->
  words_in_chapter

wodehouse <- inner_join(wodehouse, chapter_words)
wodehouse <- inner_join(wodehouse, words_in_chapter)

wodehouse %>% 
  mutate(word_freq = n/n_words) ->
  wodehouse


wodehouse %>% 
  filter(word == "сэр") %>% 
  select(chapter, word, word_freq) %>% 
  ggplot(aes(word_freq)) +
  geom_histogram(fill = "lightblue")+
  geom_density(color = "red")+
  theme_bw()+
  labs(title = 'Частотность слова "сэр" по роману П. Г. Вудхауза “Фамильная честь Вустеров”')

wodehouse %>% 
  filter(word == "сэр") %>% 
  summarise(g_mean = mean(word_freq)) ->
  grand_mean
grand_mean

### 1.2
#Посчитайте бутстрэпом доверительный интервал для средней доли слова “сэр” 
#в главах романа и выведите его размер в формате тиббл.

set.seed(42)
wodehouse %>% 
  filter(word == "сэр") ->
  wodehouse_bs

wodehouse_bs <- bootstrap(wodehouse_bs$word_freq, nboot = 10000, theta = mean)$thetastar

# ggplot работает только с датафреймами
wodehouse_bs <- data_frame(means = wodehouse_bs)  

wodehouse_bs %>% 
  ggplot(aes(means)) +
  geom_histogram(fill = "lightblue")+
  theme_bw()+
  labs(title = 'Средняя доля слова "сэр" на основе романа П. Г. Вудхауза “Фамильная честь Вустеров”',
       subtitle = "На основе 10000 бутстрэп-подвыборок")

wodehouse_bs %>%
  summarise(mean = mean(means),
            q1 = quantile(means, 0.025),
            q2 = quantile(means, 0.975))->
  wodehouse_stats
wodehouse_stats

### 1.3
#Посчитайте биномиальный доверительный интервал употребления слова “сэр” 
#в каждой главе и выведите главу с максимальным из интервалов в формате тиббл.

wodehouse %>% 
  filter(word == "сэр") %>%
  slice(1:30) %>% 
  group_by(chapter) %>% 
  mutate(low_ci = binom.test(x = n, n = n_words, ci.method = "Clopper-Pearson")$conf.int[1],
         up_ci = binom.test(x = n, n = n_words, ci.method = "Clopper-Pearson")$conf.int[2]) %>%
  ggplot(aes(chapter, word_freq))+
  geom_point()+
  geom_pointrange(aes(ymin = low_ci, ymax = up_ci))+
  theme_bw()+
  coord_flip()+
  labs(title = 'Среднее и 95% CI употребления "сэр" в романе П. Г. Вудхауза “Фамильная честь Вустеров”',
       x = "", y = "")

#сделать тиббл с максимальным
wodehouse_bs %>%
  summarise(mean = mean(means),
            q1 = quantile(means, 0.025),
            q2 = quantile(means, 0.975))->
  wodehouse_stats
wodehouse_stats


### 1.4
#Посчитайте байесовский биномиальный доверительный интервал употребления слова “сэр” 
#в каждой главе и выведите главу с максимальным из интервалов в формате тиббл.

mu <- mean(wodehouse$word_freq[wodehouse$word == "сэр"])
var <- var(wodehouse$word_freq[wodehouse$word == "сэр"])
alpha0 <- ((1 - mu) / var - 1 / mu) * mu ^ 2
beta0 <- alpha0 * (1 / mu - 1)
alpha0
beta0

wodehouse %>% 
  filter(word == "сэр") %>%
  slice(1:30) %>% 
  group_by(chapter) %>% 
  mutate(alpha_post = n+alpha0,
         beta_post = n_words-n+beta0,
         average_post = alpha_post/(alpha_post+beta_post),
         cred_int_l = qbeta(.025, alpha_post, beta_post),
         cred_int_h = qbeta(.975, alpha_post, beta_post)) ->
  posterior

posterior %>% 
  select(chapter, word, n_words, word_freq, average_post) %>% 
  arrange(n_words)

posterior %>% 
  ggplot(aes(chapter, average_post, ymin = cred_int_l, ymax = cred_int_h))+
  geom_pointrange()+
  coord_flip()+
  theme_bw()

#сделать тиббл с максимальным
wodehouse_bs %>%
  summarise(mean = mean(means),
            q1 = quantile(means, 0.025),
            q2 = quantile(means, 0.975))->
  wodehouse_stats
wodehouse_stats

### 1.5

#Посчитайте биномиальный доверительный интервал употребления слова “сэр” 
#в каждой главе и выведите главу с минимальным из интервалов в формате тиббл.

### 1.6

#Посчитайте байесовский биномиальный доверительный интервал употребления слова “сэр” 
#в каждой главе и выведите главу с минимальным из интервалов в формате тиббл.

### 1.7

#Напишите короткий текст, комментирующий наблюдаемые сходства/различия между оценками 
#среднего и доверительных интервалов количества употреблений слова “сэр” 
#во всех главах романа. Что можно сказать про разные главы? 
#Что можно сказать о сходстве/различиях фриквентистсткой и байесовской оценок
#наблюдаемых параметров?


```