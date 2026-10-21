from collections import Counter,defaultdict
import  math
import jieba

def calculate_idf(word,document):
    """计算逆文档频率"""
    doc_count= sum(1 for doc in document if word in doc )
    if doc_count == 0:
        return 0

    idf = math.log(doc_count/len(document))
    return idf

document = [
    "我喜欢python","python很有趣","我喜欢编程"
]
print("文件集：")
for i, doc in enumerate(document,1):
    print(f" file {i}. {doc}")
print("IDF calculated")

word = set()
for doc in document:
    word.update(doc.split())

for word in sorted(word):
    idf = calculate_idf(word,document)
    doc_count= sum(1 for doc in document if word in doc )
    print(f" file  {word} is {doc_count} times,idf is {idf:.3f}")
# TF-IDF的意义
# 组合	                   含义	        TF-IDF 权重	          典型词	      解读
# TF 高，IDF 高	本文档反复出现，且全语料中罕见	最高	专业术语、专有名词、领域关键词	最能代表本文档特性，是关键词抽取的首选
# TF 高，IDF 低	本文档反复出现，但全语料中也遍地都是	低	停用词、通用动词/名词：“的、是、研究、方法、the”	有“量”无“区分度”，IDF 把它压下去
# TF 低，IDF 高	全语料中罕见，但本文档只提了一两次	中等偏低	长尾实体、一次性术语、偶然出现的专名	可能是被埋没的关键线索，也可能是一次噪声
# TF 低，IDF 低	本文档出现少，且全语料中很普遍	最低	短文档里的通用词	几乎无信息量，通常直接过滤
#① TF 高，IDF 高 —— 文档的“指纹词” 这是 TF-IDF 想要捕获的目标。词在本文档密集出现，说明它是论述焦点；在全语料罕见，说明它具备区分力。例如一篇讲“硬盘坏道检测”的文档里，“坏道”反复出现而其他文档几乎不谈——它就是主题词。用途：关键词抽取、文档主题标签、检索召回的强信号。 需要警惕的例外：若某词只出现在这一篇文档里、却在文中被机器反复重复（模板、日志、爬虫灌水、OCR 错字），同样会得到“高 TF × 高 IDF”，但它只是噪声而非主题。所以单靠 TF-IDF 排序后往往还要人工或规则复核。
# ② TF 高，IDF 低 —— 通用背景词 词在本文档多，但在整个语料里也到处都是。它的高频是“语言习惯”而非“内容特性”，IDF 接近 0，乘积被压得很低。这类词就是停用词表的来源。 但不要一刀切：否定词（“不”“未”）、程度词、领域内高频但语义关键的功能词（如法律文本里的“应当”“不得”），IDF 低却承载语义，简单删除会损伤任务效果。此时应改用有监督权重或词性/位置特征，而不是硬删。
# ③ TF 低，IDF 高 —— 长尾线索或一次性噪声 词很稀有，但在本文档只出现一两次。TF-IDF 给它中等偏低的分数，不足以让它进入 top-k 关键词，于是它既可能是“被漏掉的关键实体”（文中只提了一次的核心人名、型号、地名），也可能是“拼写错误、转载残留、偶发引用”。 这类词的价值高度依赖场景：短文本（标题、微博、搜索 query）里 TF 普遍为 1，TF 几乎不提供信息，此时 IDF 与词的位置/是否在标题就成了主要判据；长文档里则更容易被淹没。想救回它，可加“首现位置”“是否在标题/摘要”“是否专名”等先验。
# ④ TF 低，IDF 低 —— 双重无信息 词在本文档出现少，在全语料里却很常见。两个因子都小，乘积最低，基本可以直接丢弃。 实务上这种组合较少见（一个语料级高频词通常在某篇文档里也不会太少，除非该文档极短），一旦出现，多半说明文档过短导致 TF 统计不稳，或该词处在分布的长尾边界。对它的正确处理就是过滤，不必可惜。
#




