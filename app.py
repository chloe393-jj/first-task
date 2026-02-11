import streamlit as st

# 1. 设置网页标题
st.set_page_config(page_title="我的记账本", page_icon="💰")
st.title("💰 简易记账小助手")

# 2. 初始化“背包”（Session State）
if 'bills' not in st.session_state:
    st.session_state.bills = []

# 3. 侧边栏：输入区域
with st.sidebar:
    st.header("📝 记一笔")
    item_type = st.radio("类型", ["支出 💸", "收入 💰"])
    amount = st.number_input("金额", min_value=0.0, step=1.0)
    note = st.text_input("备注", value="例如：买咖啡")
    
    if st.button("提交记录"):
        if amount > 0:
            final_amount = -amount if "支出" in item_type else amount
            new_bill = {"类型": item_type, "金额": final_amount, "备注": note}
            st.session_state.bills.append(new_bill)
            st.success(f"成功记录：{note} {final_amount}元")
        else:
            st.warning("金额不能是 0 哦！")

# 4. 主界面：展示数据
total_balance = sum(item['金额'] for item in st.session_state.bills)
st.metric(label="当前总余额", value=f"{total_balance:.2f} 元")

# 5. 展示详细账单
if st.session_state.bills:
    st.write("### 📜 账单明细")
    st.table(st.session_state.bills)
    
    if st.button("清空所有账单"):
        st.session_state.bills = []
        st.rerun()
else:
    st.info("还没有记账哦，快去侧边栏记一笔吧！")
