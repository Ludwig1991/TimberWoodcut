# DeepSeek-V3 分词器工具办公整理文档
## 一、核心概述
本文档为DeepSeek-V3大模型配套分词器工具的标准化办公整理内容。该工具是DeepSeek-V3模型用于将文本拆分为模型可识别token单元的核心组件，本质为模型配套的“字典”工具，**非大模型本体**，核心用于token计数、文本预处理、本地prompt合规性校验等场景。

## 二、配套文件清单
| 文件名 | 文件大小 | 核心用途 |
|--------|----------|----------|
| tokenizer.json | 7.5 MB | BPE词表核心文件，分词器的核心字典库 |
| tokenizer_config.json | 3.5 KB | 分词器核心配置文件，定义分词规则与基础参数 |
| deepseek_tokenizer.py | 277 B | 分词器本地测试脚本，实现基础分词功能 |
| token_counter.py | - | Token计数专用脚本，支持文本/文件计数、成本测算等扩展功能 |

## 三、核心技术参数
| 参数名称 | 参数值 | 补充说明 |
|----------|--------|----------|
| 词表大小 | 128,000 tokens | 128K全量词表 |
| 分词算法 | BPE (Byte Pair Encoding) | 字节对编码，大模型主流分词算法 |
| 最大上下文窗口 | 16,384 tokens | 支持16K上下文文本处理 |
| 分词器基类 | LlamaTokenizerFast | 基于Llama架构快速分词器开发 |
| 特殊token数量 | 818个 | 含工具调用专用标记 |
| 句首标记BOS | <｜begin▁of▁sentence｜> | 文本起始标识 |
| 句尾标记EOS | <｜end▁of▁sentence｜> | 文本结束标识 |

## 四、核心应用场景
1.  **Token用量测算**：精准统计文本token消耗，估算DeepSeek API调用成本；
2.  **文本预处理**：调用DeepSeek API前，对超长文本进行截断、分块处理，避免超出上下文窗口限制；
3.  **本地合规校验**：离线验证prompt、输入文本是否超出模型上下文窗口，提前规避接口调用报错；
4.  **分词效果测试**：本地验证不同语言、不同场景文本的分词效果，优化prompt编写。

## 五、环境部署与使用方法
### （一）基础环境准备
执行以下命令安装核心依赖库：
```bash
pip install transformers tokenizers
```

### （二）分词器基础用法
执行以下命令运行基础测试脚本，完成分词功能验证：
```bash
python deepseek_tokenizer.py
```

### （三）Token计数器专用脚本用法
计数器已完成编码兼容问题修复，支持多场景计数与成本测算，具体命令与对应效果如下：
| 执行命令 | 核心效果 |
|----------|----------|
| python token_counter.py "待统计文本" | 直接对输入的目标文本进行token数量统计 |
| python token_counter.py -f file.txt | 读取指定txt文件，统计全文件token数量 |
| python token_counter.py --model v3-128k -f file.txt | 基于128K上下文规则，对目标文件做token统计 |
| python token_counter.py --cost 0.27 --cost-out 1.10 -f file.txt | 按设定的输入/输出单价，测算文件API调用成本 |
| python token_counter.py -v -f file.txt | 统计token数量的同时，展示全量token拆分详情 |

## 六、实测数据与结论
### （一）分词实测数据
| 测试内容 | 字符数量 | Token数量 | 字符/Token比率 |
|----------|----------|-----------|----------------|
| MEMORY.md文档 | 1713 | 929 | 1.8 字符/token |
| 中文标准测试句 | 33 | 16 | 2.1 字符/token |
| 英文测试句“Hello world” | 11 | 2 | 5.5 字符/token |

### （二）核心结论
中文文本约**2个字符消耗1个token**，英文文本约**4-5个字符消耗1个token**，相同字符数下，中文文本的token消耗显著高于英文。

## 七、重要注意事项
原始压缩包内的`tokenizer.json`文件，直接通过transformers库加载会出现编码异常问题；改用tokenizers库直接加载.json文件可完全正常使用，当前配套脚本已自动完成该兼容问题处理，无需手动修改。

## 八、一句话核心总结
DeepSeek-V3配套128K词表BPE分词器，支持16K上下文窗口，基于Llama架构开发，内置工具调用专用模板，核心用于token计数、文本预处理，非模型本体，脚本已修复编码兼容问题，可直接部署使用。
