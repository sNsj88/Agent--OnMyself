# -*- coding: utf-8 -*-
"""
@Author: SJ.SN
@Desc:
@Time: 2026/10/21 12:34
"""
from fastapi import APIRouter
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter()
# 找到静态页面目录
_STATIC_DIR = Path(__file__).parent.parent / "static"
# 接收html页面请求css和js文件的请求，这些请求没写路由，靠匹配前缀，并去掉前缀后的字符串当文件名去static文件夹中找文件
router.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

@router.get("/", include_in_schema=False)
async def chat_page() -> FileResponse:
    return FileResponse(_STATIC_DIR / "index.html")


@router.get("/admin", include_in_schema=False)
async def admin_page() -> FileResponse:
    """后台管理首页:知识库、RAG 评估、飞轮待审、观测与成本、主题分布、分类器验收各一张卡,一处进出。
    各模块页面还是各自原本的路径,首页只把入口收到一起,文档里贴过的链接照样能用。"""
    return FileResponse(_STATIC_DIR / "admin.html")


@router.get("/kb", include_in_schema=False)
async def kb_page() -> FileResponse:
    """ch03 知识库录入页:贴文档就能切块入库、向量化、当场检索自测。"""
    return FileResponse(_STATIC_DIR / "kb.html")


@router.get("/rag-eval", include_in_schema=False)
async def rageval_page() -> FileResponse:
    """ch04 RAG 评估页:四策略对照的那份报告,页面上看,也在页面上重跑。"""
    return FileResponse(_STATIC_DIR / "rageval.html")


@router.get("/review", include_in_schema=False)
async def review_page() -> FileResponse:
    """ch09 飞轮待审队列后台管理页。"""
    return FileResponse(_STATIC_DIR / "review.html")


@router.get("/observability", include_in_schema=False)
async def observability_page() -> FileResponse:
    """ch09 观测与成本页:意图成本账、评估趋势、置信度阈值校准三张报表,页上看也页上重跑。"""
    return FileResponse(_STATIC_DIR / "observability.html")


@router.get("/topics", include_in_schema=False)
async def topics_page() -> FileResponse:
    """ch10 主题分布页:分类器旁路归类结果,按 17 类看问题量。"""
    return FileResponse(_STATIC_DIR / "topics.html")


@router.get("/topics/questions", include_in_schema=False)
async def topic_questions_page() -> FileResponse:
    """ch10 类目问题列表:从分布图点进某一类,分页看这类下归类到的全部问题。"""
    return FileResponse(_STATIC_DIR / "topic-questions.html")


@router.get("/acceptance", include_in_schema=False)
async def acceptance_page() -> FileResponse:
    """ch10 验收总览:九项实证各一张闸门卡,产物缺失就地重跑。"""
    return FileResponse(_STATIC_DIR / "acceptance.html")


@router.get("/acceptance/eval", include_in_schema=False)
async def acceptance_eval_page() -> FileResponse:
    """ch10 评测详情:每类 P/R/F1 与容错红线、micro vs macro、阈值扫描、混淆矩阵、单句试分类。"""
    return FileResponse(_STATIC_DIR / "acceptance-eval.html")


@router.get("/acceptance/data", include_in_schema=False)
async def acceptance_data_page() -> FileResponse:
    """ch10 数据产物:语料血缘、三份考卷与泄漏自检、训练与 ONNX 产物盘点。"""
    return FileResponse(_STATIC_DIR / "acceptance-data.html")


@router.get("/acceptance/errors", include_in_schema=False)
async def acceptance_errors_page() -> FileResponse:
    """ch10 错例复核:逐条标准/预测对照、错误方向记账、边界摩擦配对。"""
    return FileResponse(_STATIC_DIR / "acceptance-errors.html")

