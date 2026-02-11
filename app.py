streamlit
import streamlit as st

# 1. 设置网页标题和图标
st.set_page_config(page_title="我的记账本", page_icon="💰")
st.title("💰 简易记账小助手")

# 2. 初始化“背包”（Session State）
# 如果背包里还没有账单列表，就创建一个空的
if 'bills' not in st.session_state:
    st.session_state.bills = []

# 3. 侧边栏：输入区域
with st.sidebar:
    st.header("📝 记一笔")
    # 选择是收入还是支出
    item_type = st.radio("类型", ["支出 💸", "收入 💰"])
    # 输入金额
    amount = st.number_input("金额", min_value=0.0, step=1.0)
    # 输入备注
    note = st.text_input("备注", value="例如：买咖啡")
    
    # 确认按钮
    if st.button("提交记录"):
        if amount > 0:
            # 逻辑判断：如果是支出，就变成负数
            final_amount = -amount if "支出" in item_type else amount
            
            # 把这条数据装进“背包”里
            new_bill = {"类型": item_type, "金额": final_amount, "备注": note}
            st.session_state.bills.append(new_bill)
            
            st.success(f"成功记录：{note} {final_amount}元")
        else:
            st.warning("金额不能是 0 哦！")

# 4. 主界面：展示数据
# 计算总余额
total_balance = sum(item['金额'] for item in st.session_state.bills)

# 使用大字体展示余额
st.metric(label="当前总余额", value=f"{total_balance:.2f} 元")

# 5. 展示详细账单
if st.session_state.bills:
    st.write("### 📜 账单明细")
    # 把列表直接显示为表格
    st.table(st.session_state.bills)
    
    # 添加一个清空按钮
    if st.button("清空所有账单"):
        st.session_state.bills = []
        st.rerun() # 重新运行代码以刷新页面
else:
    st.info("还没有记账哦，快去侧边栏记一笔吧！")
