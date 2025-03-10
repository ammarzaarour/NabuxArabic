import streamlit as st


if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

if "chat_history1" not in st.session_state:
        st.session_state["chat_history1"] = []


# More specific CSS to force sidebar to right
st.markdown("""
<style>
    /* Force RTL layout for the entire app */
    .stApp {
        direction: rtl;
    }
    
    /* Target the sidebar specifically */
    section[data-testid="stSidebar"] {
        left: auto !important;
        right: 0 !important;
        direction: rtl !important;
    }
    
    /* Target the main content */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 25rem;
        max-width: 100%;
    }
    
    /* Adjust animation direction */
    .stSidebar {
        transform-origin: right !important;
    }
    
    /* Ensure sidebar toggle button is positioned correctly */
    button[kind="headerNoPadding"] {
        left: auto !important;
        right: 0 !important;
    }
    
    /* Make sure form elements and content in main area are properly aligned */
    .stTextInput, .stButton, .stSelectbox {
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)


def intro():
    from Backend.backendA import run_llm

    st.write("# أستاذ")

    # Check if the first prompt has been made
    if "first_prompt_made" not in st.session_state:
        st.session_state.first_prompt_made = False  # Track first user input
    
    # Show introduction text only if no prompt has been made
    if not st.session_state.first_prompt_made:
        st.write(" في هذه المرحلة، تتعلم ما هو الذكاء الاصطناعي، والمفاهيم الأساسية مثل التعلم الآلي، الشبكات العصبية، والرؤية الحاسوبية.")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    if "show_quick_questions" not in st.session_state:
        st.session_state.show_quick_questions = True

    st.write("")  # Adds a blank line (break)
    st.write("")  # Adds a blank line (break)
    st.write("")  # Adds a blank line (break)
    st.write("")  # Adds a blank line (break)
    st.write("")  # Adds a blank line (break)
    st.write("")  # Adds a blank line (break)

    # Quick questions section - only show if flag is True and no messages yet
    if st.session_state.show_quick_questions and len(st.session_state.messages) == 0:
       
        quick_questions = [
            "هل يمكنني إنشاء نموذج ذكاء اصطناعي بسيط دون خبرة برمجية؟",
            "ما هو الذكاء الاصطناعي، وكيف يعمل؟",
            "لماذا لا يفهم الذكاء الاصطناعي أحيانًا ما أقوله أو أكتبه؟",
            "إذا كان لديك روبوت ذكي يساعدك في حياتك اليومية، ماذا تريد منه أن يفعل؟"
        ]
        
        cols = st.columns(2)  # Create two equal-sized columns
        
        for i, question in enumerate(quick_questions):
            col_idx = i % 2  # Alternate between columns
            with cols[col_idx]:  # Assign content to the column
                with st.container():  # Ensures equal-sized buttons inside containers
                    button_key = f"quick_q_{i}"
                    if st.button(question, key=button_key, use_container_width=True):
                        # Hide quick questions
                        st.session_state.show_quick_questions = False
                        
                        # Mark that the first prompt has been made
                        st.session_state.first_prompt_made = True  
                        
                        # Set a flag to indicate we need to process this question
                        st.session_state[f"clicked_{button_key}"] = True
                        st.rerun()

    # Process button clicks from previous run
    for i in range(4):  # Check all 4 possible quick questions
        button_key = f"quick_q_{i}"
        if st.session_state.get(f"clicked_{button_key}", False):
            # Clear the flag
            st.session_state[f"clicked_{button_key}"] = False
            
            # Get the question text
            question = [
                "هل يمكنني إنشاء نموذج ذكاء اصطناعي بسيط دون خبرة برمجية؟",
                "ما هو الذكاء الاصطناعي، وكيف يعمل؟",
                "لماذا لا يفهم الذكاء الاصطناعي أحيانًا ما أقوله أو أكتبه؟",
                "إذا كان لديك روبوت ذكي يساعدك في حياتك اليومية، ماذا تريد منه أن يفعل؟"
            ][i]
            
            # Mark that the first prompt has been made
            st.session_state.first_prompt_made = True  
            
            # Add to messages and process
            st.session_state.messages.append({"role": "user", "content": question})
            
            # Generate response using the LLM
            generated_response = run_llm(
                query=question,
                chat_history=st.session_state["chat_history"]
            )
            st.session_state["chat_history"].append(("human", question))
            st.session_state["chat_history"].append(("ai", generated_response))
            st.session_state.messages.append({"role": "assistant", "content": generated_response})
            break  # Process only one click at a time

    
    
    # Display chat messages from history
    for message_data in st.session_state.messages:
        with st.chat_message(message_data["role"]):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in message_data["content"]):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{message_data["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(message_data["content"])

    # Input box for user prompt
    if prompt := st.chat_input("... اسألني شيئاً"):
        with st.chat_message("user"):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in prompt):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{prompt}</div>', unsafe_allow_html=True)
            else:
                st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response using the LLM
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history"]
            )
            st.session_state["chat_history"].append(("human", prompt))
            st.session_state["chat_history"].append(("ai", generated_response))

            with st.chat_message("assistant"):
                # Check if the generated response contains Arabic characters and render it properly
                if any("\u0600" <= char <= "\u06FF" for char in generated_response):  # Check if Arabic
                    st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{generated_response}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(generated_response)
            
            st.session_state.messages.append({"role": "assistant", "content": generated_response})


def generate_email():
    import streamlit as st
    from Backend.backendB import run_llm
    
    st.write("# أستاذ")
    
    if "messages1" not in st.session_state:
        st.session_state.messages1 = []
    

    
    # Display chat messages from history
    for message_data in st.session_state.messages1:
        with st.chat_message(message_data["role"]):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in message_data["content"]):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{message_data["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(message_data["content"])

    # Input box for user prompt
    if prompt := st.chat_input("... اسألني شيئاً"):
        with st.chat_message("user"):
            # Check if the message contains Arabic characters and render it properly
            if any("\u0600" <= char <= "\u06FF" for char in prompt):  # Check if Arabic
                st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{prompt}</div>', unsafe_allow_html=True)
            else:
                st.markdown(prompt)
        
        st.session_state.messages1.append({"role": "user", "content": prompt})

        # Generate response using the LLM
        with st.spinner("Generating response..."):
            generated_response = run_llm(
                query=prompt,
                chat_history=st.session_state["chat_history1"]
            )
            st.session_state["chat_history1"].append(("human", prompt))
            st.session_state["chat_history1"].append(("ai", generated_response))

            with st.chat_message("assistant"):
                # Check if the generated response contains Arabic characters and render it properly
                if any("\u0600" <= char <= "\u06FF" for char in generated_response):  # Check if Arabic
                    st.markdown(f'<div style="direction: rtl; font-family: Arial, sans-serif; white-space: pre-wrap;">{generated_response}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(generated_response)
            
            st.session_state.messages1.append({"role": "assistant", "content": generated_response})


def upgrade_page():
    st.write("# ترقية حسابك")
    
    # Create columns for a nice layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="direction: rtl; font-family: Arial, sans-serif;">
        <h2>اكتشف الميزات المتقدمة لأستاذ</h2>
        <p>قم بالترقية اليوم للوصول إلى جميع الميزات المتقدمة التي تساعدك على تحسين تجربتك التعليمية.</p>
        
        <h3>المميزات المتاحة في النسخة المتقدمة:</h3>
        <ul>
            <li>تدريبات متخصصة في قواعد اللغة العربية</li>
            <li>مساعدة في كتابة المقالات والأبحاث</li>
            <li>تصحيح النصوص مع شرح تفصيلي للأخطاء</li>
            <li>محادثات غير محدودة مع الذكاء الاصطناعي</li>
            <li>تمارين مخصصة حسب مستوى المستخدم</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Contact form
        st.markdown("<h3 style='direction: rtl;'>للاشتراك، يرجى ملء النموذج التالي:</h3>", unsafe_allow_html=True)
        name = st.text_input("الاسم")
        email = st.text_input("البريد الإلكتروني")
        phone = st.text_input("رقم الهاتف (اختياري)")
        
        if st.button("إرسال طلب الترقية"):
            st.success("تم استلام طلبك بنجاح! سنتواصل معك قريبًا.")
    
    with col2:
        # Pricing cards
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 15px; direction: rtl;">
            <h3>الباقة الشهرية</h3>
            <h2>$9.99 <small>/شهر</small></h2>
            <ul>
                <li>جميع الميزات المتقدمة</li>
                <li>دعم فني على مدار الساعة</li>
                <li>إلغاء الاشتراك في أي وقت</li>
            </ul>
        </div>
        
        <div style="background-color: #e9f7ef; padding: 20px; border-radius: 10px; border: 2px solid #27ae60; direction: rtl;">
            <h3>الباقة السنوية <span style="background-color: #27ae60; color: white; padding: 2px 5px; border-radius: 5px; font-size: 12px;">خصم 30%</span></h3>
            <h2>$69.99 <small>/سنة</small></h2>
            <ul>
                <li>جميع الميزات المتقدمة</li>
                <li>دعم فني على مدار الساعة</li>
                <li>محتوى حصري إضافي</li>
                <li>تحديثات مجانية</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


with st.sidebar:
    
    st.sidebar.image("img/NabuX1.png", width=250) 
    st.write("من الفضول الى الخبرة، اكتشف وتعلم الذكاء الاصطناعي")

    page_names_to_funcs = {
        "انطلق في عالم المعرفة": intro,
        "تعمّق في جوهر الفهم": generate_email,
        # Add the new options with the upgrade_page function for all locked options
        "حوّل المعرفة إلى فعل مبدع": upgrade_page,
        "استكشف أسرار التحليل العميق": upgrade_page,
        "صقل قدراتك بالتقييم المستمر": upgrade_page,
         "أطلق العنان لإبداعك وتصدر القمة": upgrade_page
    }
    
    # List of only the unlocked options
    unlocked_options = ["انطلق في عالم المعرفة", "تعمّق في جوهر الفهم"]
    
    # Function to format the option text (add a lock symbol to locked options)
    def format_option(option):
        if option in unlocked_options:
            return option
        else:
            return f"{option} 🔒"
    
    # Format all options for display
    formatted_options = [format_option(option) for option in page_names_to_funcs.keys()]
    
    # Display the selectbox with formatted options
    selected_formatted = st.sidebar.selectbox("### **اختر المستوى**", formatted_options)
    
    # Get the original option name (without the lock symbol)
    selected_option = list(page_names_to_funcs.keys())[formatted_options.index(selected_formatted)]
    
    # Set the selected option/function to use
    demo_name = selected_option
    
    # Rest of your sidebar code
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("محادثة جديدة"):
            st.session_state.messages = []
            st.session_state.email_drafts = []
            st.session_state["chat_history"] = []

    # Add upgrade button in the sidebar
    if selected_option not in unlocked_options:
        st.info("هذه الميزة متاحة فقط للمشتركين في الباقة المدفوعة", icon="ℹ️")
        
    st.markdown("---")
    st.write("© 2025 أستاذ. All rights reserved.")
    st.markdown(
        """
        <p>
        <a href="https://github.com/" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png"/>
        </a>
        <a href="https://t.me/telegram_channel" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/telegram-app.png"/>
        </a>
        <a href="" target="_blank">
        <img src="https://img.icons8.com/ios-glyphs/30/000000/email.png"/>
        </a>
        </p>
        """, unsafe_allow_html=True
    )

# Call the appropriate function based on the selected option
page_names_to_funcs[demo_name]()