import gradio as gr
from stats import get_dashboard_stats,get_all_topics,get_all_companies
from search.search_engine import search
from tracker.progress import sync_solved_problems
from auth.auth import create_user,login_user
def clear_filters():
    return None,None,None,50,False


def update_progress(selected_boxes, user_id, visible_problem_ids):
    if user_id is None:
        return "Please login first"
    selected_ids = [
        visible_problem_ids[title]
        for title in selected_boxes
    ]
    visible_ids = list(visible_problem_ids.values())
    sync_solved_problems(user_id, selected_ids, visible_ids)
    return "Progress updated successfully"



def run_search(company, topic, difficulty, limits,user_id,show_solved):
    results,solved_ids = search(company, topic, difficulty, limits,user_id,show_solved)
    if not results:
        return "No results found.", gr.update(choices=[], value=[]), {},""

    output = ""
    visible_problem_ids = {}
    problem_choices = []
    selected = []
    for problem in results:
        problem_id, title, diff, freq, link = problem

        output += f"""
    ### {title}
    - Difficulty: {diff}
    - Link: {link}
    ---
    """

        visible_problem_ids[title] = problem_id
        choice = title
        problem_choices.append(choice)

        if problem_id in solved_ids:
            selected.append(choice)

    return (
        output,
        gr.update(
            choices=problem_choices,
            value=selected
        ),
        visible_problem_ids,
        ""
    )

def sign_up(username,password):
    return create_user(username,password)

def login(username, password):
    user_id = login_user(username, password)

    if user_id:
        return (
            "Login successful",
            user_id,
            gr.update(visible=False),
            gr.update(visible=True)
        )

    return (
        "Invalid credentials",
        None,
        gr.update(),
        gr.update()
    )


stats=get_dashboard_stats()
topics=get_all_topics()
comp=get_all_companies()

with gr.Blocks() as demo:
    current_user = gr.State(None)
    visible_problems_state = gr.State({})

    # ============================================================
    # LOGIN SECTION
    # ============================================================
    with gr.Row():
        with gr.Column(scale=1):
            pass
        with gr.Column(scale=2):
            with gr.Column(visible=True) as login_section:

                gr.HTML("""
                <style>
                    .lci-login-wrap {
                        max-width: 460px;
                        margin: 40px auto 0 auto;
                        padding: 36px 32px 28px 32px;
                        background: linear-gradient(180deg, #1a1a1a 0%, #161616 100%);
                        border: 1px solid #2a2a2a;
                        border-radius: 18px;
                        box-shadow: 0 8px 30px rgba(0,0,0,0.45);
                        text-align: center;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    }
                    .lci-brand {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                        margin-bottom: 4px;
                    }
                    .lci-brand-icon {
                        width: 34px;
                        height: 34px;
                        border-radius: 9px;
                        background: linear-gradient(135deg, #FFA116, #FF6B00);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 700;
                        font-size: 18px;
                        color: #161616;
                    }
                    .lci-title {
                        font-size: 24px;
                        font-weight: 700;
                        color: #f5f5f5;
                        letter-spacing: -0.3px;
                        margin: 0;
                    }
                    .lci-subtitle {
                        color: #9a9a9a;
                        font-size: 14px;
                        margin: 6px 0 22px 0;
                        line-height: 1.5;
                    }
                    .lci-howto {
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        gap: 10px;
                        background: #1f1a14;
                        border: 1px solid rgba(255,161,22,0.35);
                        border-radius: 12px;
                        padding: 12px 16px;
                        margin-bottom: 24px;
                        text-align: left;
                    }
                    .lci-howto-text {
                        font-size: 13.5px;
                        color: #e0e0e0;
                    }
                    .lci-howto-text strong {
                        color: #FFA116;
                        display: block;
                        font-size: 13px;
                        margin-bottom: 2px;
                    }
                    .lci-howto a {
                        background: #FFA116;
                        color: #161616 !important;
                        font-weight: 600;
                        font-size: 13px;
                        padding: 7px 14px;
                        border-radius: 8px;
                        text-decoration: none;
                        white-space: nowrap;
                        transition: opacity 0.15s ease;
                    }
                    .lci-howto a:hover {
                        opacity: 0.85;
                    }
                    .lci-divider {
                        border: none;
                        border-top: 1px solid #2a2a2a;
                        margin: 22px 0 18px 0;
                    }
                </style>

                <div class="lci-login-wrap">
                    <div class="lci-brand">
                        <div class="lci-brand-icon">⌘</div>
                        <p class="lci-title">LeetCode Interview Intelligence</p>
                    </div>
                    <p class="lci-subtitle">
                        Sign in to access your personalized interview prep dashboard
                    </p>

                    <div class="lci-howto">
                        <div class="lci-howto-text">
                            <strong>New here?</strong>
                            Learn how this platform works in 2 minutes
                        </div>
                        <a href="https://singular-druid-42f286.netlify.app" target="_blank">
                            How it works →
                        </a>
                    </div>

                    <hr class="lci-divider">
                </div>
                """)

                username = gr.Textbox(label="Username")
                password = gr.Textbox(label="Password", type="password")

                with gr.Row():
                    sign_up_button = gr.Button("Signup")
                    login_button = gr.Button("Login")

                auth_output = gr.Markdown()

        with gr.Column(scale=1):
            pass

    # ============================================================
    # APP / DASHBOARD SECTION
    # ============================================================
    with gr.Column(visible=False) as app_section:

        gr.HTML(f"""
        <style>
            .lci-dash-header {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                margin-bottom: 22px;
            }}
            .lci-dash-title-row {{
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 18px;
            }}
            .lci-dash-icon {{
                width: 36px;
                height: 36px;
                border-radius: 9px;
                background: linear-gradient(135deg, #FFA116, #FF6B00);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 18px;
                color: #161616;
                flex-shrink: 0;
            }}
            .lci-dash-title {{
                font-size: 22px;
                font-weight: 700;
                color: #f5f5f5;
                letter-spacing: -0.3px;
                margin: 0;
            }}
            .lci-dash-sub {{
                font-size: 13px;
                color: #888;
                margin: 2px 0 0 0;
            }}
            .lci-stats-grid {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 14px;
            }}
            .lci-stat-card {{
                background: linear-gradient(180deg, #1a1a1a 0%, #161616 100%);
                border: 1px solid #2a2a2a;
                border-radius: 14px;
                padding: 16px 14px;
                text-align: center;
                transition: border-color 0.15s ease, transform 0.15s ease;
            }}
            .lci-stat-card:hover {{
                border-color: #3a3a3a;
                transform: translateY(-2px);
            }}
            .lci-stat-value {{
                font-size: 24px;
                font-weight: 700;
                color: #f5f5f5;
                margin: 0 0 4px 0;
            }}
            .lci-stat-label {{
                font-size: 11.5px;
                color: #888;
                text-transform: uppercase;
                letter-spacing: 0.4px;
                margin: 0;
            }}
            .lci-stat-card.total .lci-stat-value {{ color: #FFA116; }}
            .lci-stat-card.easy .lci-stat-value {{ color: #00b8a3; }}
            .lci-stat-card.medium .lci-stat-value {{ color: #ffc01e; }}
            .lci-stat-card.hard .lci-stat-value {{ color: #ff375f; }}
            @media (max-width: 900px) {{
                .lci-stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            }}
        </style>

        <div class="lci-dash-header">
            <div class="lci-dash-title-row">
                <div class="lci-dash-icon">⌘</div>
                <div>
                    <p class="lci-dash-title">LeetCode Interview Intelligence</p>
                    <p class="lci-dash-sub">Real-time question stats across companies and topics</p>
                </div>
            </div>

            <div class="lci-stats-grid">
                <div class="lci-stat-card total">
                    <p class="lci-stat-value">{stats['total_questions']}</p>
                    <p class="lci-stat-label">Total Questions</p>
                </div>
                <div class="lci-stat-card total">
                    <p class="lci-stat-value">{stats['total_companies']}</p>
                    <p class="lci-stat-label">Companies</p>
                </div>
                <div class="lci-stat-card easy">
                    <p class="lci-stat-value">{stats['easy']}</p>
                    <p class="lci-stat-label">Easy</p>
                </div>
                <div class="lci-stat-card medium">
                    <p class="lci-stat-value">{stats['medium']}</p>
                    <p class="lci-stat-label">Medium</p>
                </div>
                <div class="lci-stat-card hard">
                    <p class="lci-stat-value">{stats['hard']}</p>
                    <p class="lci-stat-label">Hard</p>
                </div>
            </div>
        </div>
        """)
        company_input = gr.Dropdown(choices=comp, label="Company")
        topic_dropdown = gr.Dropdown(choices=topics, label="Topic")
        difficulty_dropdown = gr.Dropdown(choices=["EASY", "MEDIUM", "HARD"])

        limit = gr.Slider(minimum=10,
                          maximum=200,
                          value=20,
                          step=5,
                          label="Maximum number of questions")
        show_solved = gr.Checkbox(label="Show Solved Problems")
        search_button = gr.Button("Search")
        clear_button = gr.Button("Clear")
        with gr.Row():
            with gr.Column(scale=3):
                results = gr.Markdown(label="Results")

            with gr.Column(scale=2):
                progress_output = gr.Textbox(label="Progress Status")
                solved_boxes = gr.CheckboxGroup(label="Solved Problems")
                update_progress_button = gr.Button("Update Progress")

        search_button.click(
            fn=run_search,
            inputs=[
                company_input,
                topic_dropdown,
                difficulty_dropdown,
                limit,
                current_user,
                show_solved
            ],
            outputs=[results, solved_boxes, visible_problems_state, progress_output]
        )
        clear_button.click(fn=clear_filters, outputs=[company_input, topic_dropdown, difficulty_dropdown, limit,show_solved])
        update_progress_button.click(
            fn=update_progress,
            inputs=[solved_boxes, current_user, visible_problems_state],
            outputs=progress_output
        )
    sign_up_button.click(
        fn=sign_up,
        inputs=[username, password],
        outputs=auth_output
    )
    login_button.click(
        fn=login,
        inputs=[username, password],
        outputs=[
            auth_output,
            current_user,
            login_section,
            app_section
        ]
    )

    demo.launch(share=True)



