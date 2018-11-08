
# coding: utf-8

# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import matplotlib.pyplot as plt
import time

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']


"""
函数说明：使用文本注解绘制树节点

1.plotNode函数

Parameters: 
    nodeTxt 决策树
    centerPt 最优特征标签
    parentPt 测试数据列表
    nodeType 节点格式
Returns: 
    无
    
Tips:
    iter()生成迭代器，next(iter())返回迭代器的下一个项目
    matplotlib.rcParams 配置参数添加中文字体
    
Author:
    ZLin

Modify:
    2018-11-07
    
2.createPlot函数

Parameters: 
    无
    
Returns: 
    无
    
Tips:
    annotate 标注文字
    annotate 语法说明 ：annotate(s='str' ,xy=(x,y) ,xytext=(l1,l2) ,..)
    s 为注释文本内容 此处为nodeTxt
    xy 为原始坐标点
    xytext 为注释文字的坐标位置
    xycoords 参数如下:
        figure points        points from the lower left of the figure 点在图左下方
        figure pixels        pixels from the lower left of the figure 图左下角的像素
        figure fraction       fraction of figure from lower left 左下角数字部分
        axes points         points from lower left corner of axes 从左下角点的坐标
        axes pixels         pixels from lower left corner of axes 从左下角的像素坐标
        axes fraction        fraction of axes from lower left 左下角部分
        data              use the coordinate system of the object being annotated(default) 使用的坐标系统被注释的对象（默认）
        polar(theta,r)       if not native ‘data’ coordinates t
    va 
    ha 
    bbox
    arrowprops 
    
    plt.figure(num) :figure -> Top level container for all plot elements.num代表编号，不指定则默认新建一个图形，图形编号递增
 
Author:
    ZLin

Modify:
    2018-11-07    
    
"""

#定义文本框和箭头格式
decisionNode = dict(boxstyle = "sawtooth", fc = "0.8")
leafNode = dict(boxstyle = "round4", fc = "0.8")
arrow_args = dict(arrowstyle = "<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    #执行实际的绘图功能，该函数需要一个绘图区，该区域由全局变量creatPlot.ax1定义
    createPlot.ax1.annotate(nodeTxt, xy = parentPt, xycoords = 'axes fraction', xytext = centerPt, textcoords = 'axes fraction', 
                           va = "center", ha = "center", bbox = nodeType, arrowprops = arrow_args)
    
def createPlot(inTree):
    #新建一个图形，面板颜色
    fig = plt.figure(1, facecolor = 'white')
    #??
    fig.clf()
    axprops = dict(xticks = [], yticks = []) 
    createPlot.ax1 = plt.subplot(111, frameon = False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = - 0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    #plotNode('决策节点', (0.5, 0.1), (0.1, 0.5), decisionNode)
    #plotNode('叶节点', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()
    
"""
函数说明：获取叶节点的数目

Parameters: 
    myTree 决策树

Return: 
    numLeafs 叶节点数目
    
Tips:
    使用Python自带的type()函数可以判断子节点是否为字典类型
      
Author:
    ZLin

Modify:
    2018-11-07

"""

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree)[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        #判断是否是字典类型，是，则该节点也是一个判断节点，需要递归getNumLeafs()函数
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            #累计叶子节点个数
            numLeafs += 1
    return numLeafs


"""
函数说明：计算遍历过程中遇到判断节点的个数，即树的深度

Parameters: 
    myTree 决策树

Return: 
    maxDepth 树的深度
    
Tips:
      
Author:
    ZLin

Modify:
    2018-11-07

"""
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree)[0]
    #获取下一组字典
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            #更新深度
            maxDepth = thisDepth
    return maxDepth

#输出预先存储的树信息，测试用
def retrieveTree(i):
    listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},{
        'no surfacing':{0:'no', 1: {'flippers':{ 0 : {'head':{ 0:'no',1:'yes'}},1:'no'}}}
    }]
    return listOfTrees[i]

#在父节点间填充文本信息
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
    #计算树的宽度
    numLeafs = getNumLeafs(myTree)
    #获取树的高度
    depth = getTreeDepth(myTree)
    #下一个字典
    firstStr = list(myTree)[0]
    #中心位置，plotTree.totalW存储树的宽度
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    #标注有向边属性
    plotMidText(cntrPt, parentPt, nodeTxt)
    #绘制节点
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    #下一个字典
    secondDict = myTree[firstStr]
    #减少y偏移
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            #不是叶子节点，递归执行
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            #如果是叶结点，绘制叶结点，并标注有向边属性值
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
    

    
# if __name__ == '__main__':
#     start = time.clock()
#     retrieveTree(1)
#     myTree = retrieveTree(0)
#     print(myTree)
#     num = getNumLeafs(myTree)
#     print(num)
#     depth = getTreeDepth(myTree)
#     print(depth)
#     createPlot(myTree)
#     end = time.clock()
#     print("程序运行时间：%s 秒" % (end - start))

