3DMisBench

近年来，有许多建议 为了提高其性能，对著名的U-Net架构进行了修改。这项工作的核心动机是在相同的条件下对U-Net及其五个扩展进行公平的比较。及其五个扩展的相同条件进行公平的比较，以区分模型结构、模型训练和参数设置对模型性能的影响。和参数设置对训练后的模型性能的影响。
模型的影响。为此，这六种分割模型中的每一种 架构都是在相同的九个数据集上进行训练。这些 数据集被选择来涵盖各种成像模式
(X射线、计算机断层扫描、磁共振成像)、单级和多级分割问题以及 单一和多模态输入。在训练过程中，它
确保数据预处理，将数据集分成 训练、验证和测试子集、优化器、学习率变化策略、结构深度、损失函数。
监督和推理对于所有的 架构进行比较。性能的评估是以 Dice系数、表面Dice系数、平均表面距 距离、Hausdorff距离、训练和预测时间。本实验研究的主要贡献是证明了架构变体并没有改善与基本推理有关的 与基本U-Net结构相关的推理质量
而资源需求上升。




近年来，有许多不同结构的深度学习模型被提出并用于通用3D医疗影像分割。

不同模型在训练过程的数据预处理、超参数选择、损失函数、优化策略等缺乏统一的标准，因此难以比较各个模型的性能。

同时，不同数据集规模及任务特性差异，也导致单一任务的测试难以反映模型的综合性能，包括不同模型在不同分割目标（如器官、GTV）上的性能表现差异、利用数据的效率。

我们提出了一个通用的3D医疗影像分割框架，并选取了5个具有代表性的医疗影像公开数据集，这些数据集的选取涵盖不同规模、不同任务、不同成像模式(CT、PET、MRI)以及单模态和多模态输入。

我们在选取的数据集上对现有主流分割模型结构进行测试，用于对比这些模型在不同数据集规模和任务特性下的性能表现。

性能的评估基于Dice系数、平均表面距离、Hausdorff距离以及不同任务、不同数据集规模下的精度差异。

本研究的主要贡献是给出了一套相对全面和客观的通用3D医疗影像分割深度学习模型评价体系，并对几种具有代表性的主流模型进行了测试和分析。