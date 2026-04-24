"""Plan mode module - 三步编码模式实现"""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from deep_code.i18n import t

__all__ = ["run_plan_mode"]


def run_plan_mode(user_question: str, config, console: Console) -> None:
    """Execute the 3-step plan mode: optimize question → confirm plan → execute.

    Args:
        user_question: The original user question
        config: Application configuration
        console: Rich console for output
    """
    from langchain_openai import ChatOpenAI

    console.print(Panel(
        f"{t('plan_mode_desc')}",
        title=t("plan_mode_title"),
        border_style="cyan",
    ))
    console.print()

    # Get the model for plan mode
    if config.provider == "openai-like":
        model = ChatOpenAI(
            model=config.model_name,
            base_url=config.base_url,
            api_key=config.api_key,
        )
    else:
        try:
            from langchain_anthropic import ChatAnthropic
            model = ChatAnthropic(model=config.model_name)
        except ImportError:
            console.print(t("plan_model_create_error"))
            return

    # ── Step 1: Optimize the question ──────────────────────────────────────
    console.print(t("plan_step1_prompt"))

    from langchain_core.messages import HumanMessage

    optimize_messages = [
        HumanMessage(content=f"原始问题：{user_question}\n\n请优化这个问题，使其更清晰、更具体。"),
    ]
    try:
        response = model.invoke(optimize_messages)
        optimized_question = response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        console.print(t("plan_optimize_error", error=str(e)))
        return

    console.print(Markdown(optimized_question))
    console.print(t("plan_confirm"))

    try:
        confirm = console.input("> ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        console.print(f"\n[dim]{t('plan_cancel')}[/dim]")
        return

    if confirm.lower() not in ("y", "yes", ""):
        if confirm:
            optimize_messages.append(HumanMessage(content=f"用户反馈：{confirm}\n\n请根据反馈重新优化问题。"))
            try:
                response = model.invoke(optimize_messages)
                optimized_question = response.content if hasattr(response, 'content') else str(response)
            except Exception as e:
                console.print(t("plan_regenerate_error", error=str(e)))
                return
            console.print(Markdown(optimized_question))
            console.print(t("plan_confirm"))
            try:
                confirm = console.input("> ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                console.print(f"\n[dim]{t('plan_cancel')}[/dim]")
                return
            if confirm.lower() not in ("y", "yes", ""):
                console.print(t("plan_cancel"))
                console.print(t("plan_restart"))
                return
        else:
            console.print(t("plan_cancel"))
            console.print(t("plan_restart"))
            return

    # ── Step 2: Generate and confirm the plan ───────────────────────────────
    console.print(t("plan_step2_prompt"))

    plan_messages = [
        HumanMessage(content=f"已确认的问题：\n{optimized_question}\n\n请生成一个详细的实现方案，使用 markdown 格式输出，包括：\n1. 步骤列表\n2. 关键文件修改\n3. 代码示例\n4. 预期结果"),
    ]
    try:
        response = model.invoke(plan_messages)
        plan_content = response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        console.print(t("plan_generate_error", error=str(e)))
        return

    console.print(Markdown(plan_content))
    console.print(t("plan_confirm"))

    try:
        confirm = console.input("> ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        console.print(f"\n[dim]{t('plan_cancel')}[/dim]")
        return

    if confirm.lower() not in ("y", "yes", ""):
        if confirm:
            plan_messages.append(HumanMessage(content=f"用户反馈：{confirm}\n\n请根据反馈重新生成方案。"))
            try:
                response = model.invoke(plan_messages)
                plan_content = response.content if hasattr(response, 'content') else str(response)
            except Exception as e:
                console.print(t("plan_regenerate_plan_error", error=str(e)))
                return
            console.print(Markdown(plan_content))
            console.print(t("plan_confirm"))
            try:
                confirm = console.input("> ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                console.print(f"\n[dim]{t('plan_cancel')}[/dim]")
                return
            if confirm.lower() not in ("y", "yes", ""):
                console.print(t("plan_cancel"))
                console.print(t("plan_restart"))
                return
        else:
            console.print(t("plan_cancel"))
            console.print(t("plan_restart"))
            return

    # ── Step 3: Execute the plan ────────────────────────────────────────────
    console.print(t("plan_step3_exec"))

    execute_messages = [
        HumanMessage(content=f"已确认的方案：\n{plan_content}\n\n请严格按照方案执行每一步操作。使用文件系统和执行工具完成任务。"),
    ]
    try:
        response = model.invoke(execute_messages)
        execute_result = response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        console.print(t("plan_execute_error", error=str(e)))
        return

    console.print(Markdown(execute_result))
    console.print()
    console.print(t("plan_success"))
