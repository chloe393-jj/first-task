import streamlit as st
import time

# --------------------------
# 1. 页面基础设置
# --------------------------
st.set_page_config(page_title="恋爱专属空间", page_icon="❤️")

# 这是一个让页面更好看的小魔法（CSS样式）
st.markdown("""
    <style>
    .big-name {
        font-size: 50px !important;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        padding: 20px;
    }
    .score-card {
        background-color: #ffe6e6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #ffcccc;
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------
# 2. 数据初始化（背包）
# --------------------------
if 'love_score' not in st.session_state:
    st.session_state.love_score = 50  # 初始好感度
if 'history' not in st.session_state:
    st.session_state.history = []     # 历史记录
if 'boyfriend_name' not in st.session_state:
    st.session_state.boyfriend_name = "" # 名字

# --------------------------
# 3. 登录界面（第一眼看到的）
# --------------------------
if st.session_state.boyfriend_name == "":
    st.title("🔒 专属空间登录")
    st.write("请输入那个笨蛋的名字来解锁：")
    name_input = st.text_input("你的名字是？")
    
    if st.button("解锁进入 ❤️"):
        if name_input:
            st.session_state.boyfriend_name = name_input
            st.toast(f"欢迎回家，{name_input}！", icon="🏠")
            time.sleep(1)
            st.rerun() # 刷新进入主页
        else:
            st.warning("不可以不写名字哦！")

# --------------------------
# 4. 主界面（解锁后看到的）
# --------------------------
else:
    # 顶部：大大的名字展示
    st.markdown(f'<div class="big-name">To: {st.session_state.boyfriend_name} 💖</div>', unsafe_allow_html=True)
    
    # 显示当前的等级称号
    score = st.session_state.love_score
    if score < 60:
        level = "🌱 需多加呵护的幼苗"
    elif score < 100:
        level = "🌹 正在热恋的玫瑰"
    else:
        level = "💎 坚不可摧的钻石羁绊"
    
    st.caption(f"当前羁绊等级：{level}")

    # 中间：巨大的好感度显示卡片
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <div class="score-card">
            <h3>当前好感度</h3>
            <h1 style='color: #FF4B4B; font-size: 60px;'>{score}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.divider() # 分割线

    # 操作区：加分或减分
    st.subheader("📝 羁绊记录仪")
    
    with st.form("love_form"):
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            change_val = st.number_input("增减分值 (负数表示扣分)", step=1, value=10)
        with col_input2:
            reason = st.text_input("原因", placeholder="比如：今天帮我吹头发...")
            
        submitted = st.form_submit_button("💖 提交记录")
        
        if submitted:
            # 更新分数
            st.session_state.love_score += change_val
            
            # 记录历史
            timestamp = time.strftime("%Y-%m-%d %H:%M")
            emoji = "😡" if change_val < 0 else "🥰"
            new_record = f"{timestamp} | {emoji} {reason} | 变动: {change_val:+d}"
            st.session_state.history.insert(0, new_record) # 最新的排最前
            
            # 特效：如果是加分，放气球！
            if change_val > 0:
                st.balloons()
                st.success(f"好耶！好感度增加了 {change_val} 分！")
            else:
                st.error(f"哼！好感度减少了 {abs(change_val)} 分！要反省哦！")
            
            time.sleep(1)
            st.rerun()

    # 底部：历史记录列表
    st.subheader("📜 我们的点点滴滴")
    if st.session_state.history:
        for record in st.session_state.history:
            st.text(record)
    else:
        st.info("还没有记录哦，快去创造回忆吧！")

    # --- 🎁 彩蛋区域 ---
    if st.session_state.love_score >= 100:
        st.divider()
        st.balloons() # 再次庆祝
        st.warning("🎉 恭喜达成 100 分成就！解锁隐藏情书！")
        st.markdown(f"""
        > **给亲爱的 {st.session_state.boyfriend_name}：** > 既然你看到了这里，说明你对我超级好！  
        > 谢谢你的包容和爱，未来的日子也要一起努力哦！💕
        """)
    
    # 退出登录按钮（在侧边栏）
    if st.sidebar.button("退出/重置名字"):
        st.session_state.boyfriend_name = ""
        st.rerun()
