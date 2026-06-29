import gradio as gr
from stats import get_dashboard_stats,get_all_topics,get_all_companies
from search.search_engine import search
from tracker.progress import mark_solved, unmark_solved
from auth.auth import create_user,login_user
def clear_filters():
    return None,None,None,50,False

def update_progress(selected_boxes, user_id, visible_problem_ids):
    if user_id is None:
        return "Please login first"

    selected_ids = set()

    for title in selected_boxes:
        problem_id = visible_problem_ids[title]
        selected_ids.add(problem_id)

    for problem_id in visible_problem_ids.values():
        if problem_id in selected_ids:
            mark_solved(user_id, problem_id)
        else:
            unmark_solved(user_id, problem_id)

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
    with gr.Row():
        with gr.Column(scale=1):
            pass
        with gr.Column(scale=2):
            with gr.Column(visible=True) as login_section:
                gr.Markdown("# Login")

                gr.HTML("""
                <p style="text-align:center; font-size:16px;">
                    For knowing how this website works,
                    <a href="https://singular-druid-42f286.netlify.app" target="_blank">
                        Click Here
                    </a>
                </p>
                """)

                username = gr.Textbox(label="Username")
                password = gr.Textbox(label="Password", type="password")

                with gr.Row():
                    sign_up_button = gr.Button("Signup")
                    login_button = gr.Button("Login")

                auth_output = gr.Markdown()

        with gr.Column(scale=1):
            pass





    with gr.Column(visible=False) as app_section:
        gr.Markdown(f"""
            # LeetCode Intelligence

            ### Stats
            - Total Questions: {stats['total_questions']}
            - Total Companies: {stats['total_companies']}
            - Easy: {stats['easy']}
            - Medium: {stats['medium']}
            - Hard: {stats['hard']}
            """)
        stats = get_dashboard_stats()
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



