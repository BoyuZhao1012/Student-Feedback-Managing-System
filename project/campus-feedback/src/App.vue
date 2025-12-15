<template>
  <div>
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="navbar-left">
        <span class="navbar-title-bg">校园反馈系统</span>
        <span v-if="currentUser" class="role-title">{{ getRoleTitle(currentUser.role) }}</span>
      </div>
      <div v-if="currentUser" class="navbar-user">
        <span class="user-info">当前登录用户：{{ currentUser.username }} ({{ currentUser.role }})</span>
        <button @click="handleLogout" class="logout-btn">退出登录</button>
      </div>
    </nav>
    <div class="app-container" :style="backgroundStyle">
      <div class="content-wrapper">
        <!-- 未登录状态 -->
        <div v-if="!currentUser">
          <!-- 登录界面 -->
          <div v-if="!showRegister">
            <div class="login-form">
              <h4>登录</h4>
              <div class="form-group">
                <input v-model="loginName" placeholder="用户名" class="form-input">
              </div>
              <div class="form-group">
                <input v-model="loginPassword" type="password" placeholder="密码" class="form-input">
              </div>
              <div v-if="loginError" class="error-message">{{ loginError }}</div>
              <button @click="handleLogin" class="login-btn">登录</button>
              <button @click="showRegister = true" class="register-btn">注册新用户</button>
            </div>
          </div>

          <!-- 注册界面 -->
          <div v-else>
            <div class="register-form">
              <h3>注册新用户</h3>
              <div class="form-group">
                <label>用户名</label>
                <input v-model="registerData.username" placeholder="请输入用户名" class="form-input">
              </div>
              <div class="form-group">
                <label>密码</label>
                <input v-model="registerData.password" type="password" placeholder="请输入密码" class="form-input">
              </div>
              <div class="form-group">
                <label>确认密码</label>
                <input v-model="registerData.confirmPassword" type="password" placeholder="请再次输入密码" class="form-input">
              </div>
              <div class="form-group">
                <label>选择角色</label>
                <select v-model="registerData.role" class="form-input">
                  <option value="">请选择角色</option>
                  <option value="student">学生</option>
                  <option value="admin">管理员</option>
                  <option value="supervisor">总负责人</option>
                  <option value="specialist">专项负责人</option>
                </select>
              </div>
              <div v-if="registerError" class="error-message">{{ registerError }}</div>
              <div v-if="registerSuccess" class="success-message">{{ registerSuccess }}</div>
              <div class="button-group">
                <button @click="handleRegister" class="register-btn">注册</button>
                <button @click="showRegister = false" class="cancel-btn">返回登录</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 已登录状态 -->
        <div v-else>
          <!-- 学生界面 -->
          <div v-if="currentUser && currentUser.role === 'student'">
            <!-- 功能导航 -->
            <div class="nav-tabs">
              <button 
                :class="['nav-tab', { active: activeTab === 'submit' }]"
                @click="activeTab = 'submit'">
                提交新反馈
              </button>
              <button 
                :class="['nav-tab', { active: activeTab === 'my' }]"
                @click="activeTab = 'my'">
                我的反馈
              </button>
              <button 
                :class="['nav-tab', { active: activeTab === 'public' }]"
                @click="activeTab = 'public'">
                公开反馈
              </button>
            </div>
            
            <!-- 提交反馈表单 -->
            <div v-if="activeTab === 'submit'" class="feedback-form">
              <h4>提交新反馈</h4>
              <div class="form-group">
                <input v-model="newFeedback.title" placeholder="反馈标题" class="form-input">
              </div>
              <div class="form-group">
                <select v-model="newFeedback.category" class="form-input">
                  <option value="">选择反馈类别</option>
                  <option value="academic">学术问题</option>
                  <option value="facility">设施问题</option>
                  <option value="service">服务问题</option>
                  <option value="other">其他问题</option>
                </select>
              </div>
              <div class="form-group">
                <textarea v-model="newFeedback.content" placeholder="反馈内容" class="form-input"></textarea>
              </div>
              <button @click="handleSubmitFeedback" class="submit-btn">提交反馈</button>
            </div>
            
            <!-- 我的反馈列表 -->
            <div v-if="activeTab === 'my'" class="feedback-list">
              <h4>我的反馈</h4>
              <div class="feedback-grid">
                <div v-for="feedback in feedbacks" 
                     :key="feedback.id" 
                     :class="['feedback-card', { 'expanded': selectedFeedback?.id === feedback.id }]"
                     @click="toggleFeedbackDetail(feedback)">
                  <div class="card-header">
                    <h5>{{ feedback.title }}</h5>
                    <div class="status-group">
                      <span :class="['status', feedback.status]">{{ getStatusText(feedback.status) }}</span>
                      <span :class="['public-status', { 'is-public': feedback.is_public }]">
                        {{ feedback.is_public ? '已公开' : '未公开' }}
                      </span>
                    </div>
                  </div>
                  <div class="card-content">
                    <p class="card-category">{{ getCategoryText(feedback.category) }}</p>
                    <p class="card-time">提交时间：{{ formatDate(feedback.created_at) }}</p>
                    <div class="public-option">
                      <label>
                        <input
                          type="checkbox"
                          :checked="feedback.is_public"
                          @change="handleTogglePublic(feedback)"
                        >
                        公开此反馈
                      </label>
                    </div>
                  </div>
                  <!-- 展开的详情内容 -->
                  <div v-if="selectedFeedback?.id === feedback.id" class="card-details">
                    <div class="detail-section">
                      <h4>基本信息</h4>
                      <p class="detail-content">{{ feedback.content }}</p>
                      <div class="detail-meta">
                        <span>类别：{{ getCategoryText(feedback.category) }}</span>
                        <span>状态：{{ getStatusText(feedback.status) }}</span>
                        <span>提交时间：{{ formatDate(feedback.created_at) }}</span>
                      </div>
                    </div>
                    
                    <div class="detail-section">
                      <h4>处理进度</h4>
                      <div class="progress-timeline">
                        <!-- 初始提交 -->
                        <div class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">提交反馈</span>
                              <span class="timeline-time">{{ formatDate(feedback.created_at) }}</span>
                            </div>
                            <div class="timeline-comment">{{ feedback.content }}</div>
                          </div>
                        </div>

                        <!-- 管理员审核 -->
                        <div v-if="feedback.admin_comment" class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">管理员审核</span>
                              <span class="timeline-time">{{ formatDate(feedback.updated_at) }}</span>
                            </div>
                            <div class="timeline-comment">{{ feedback.admin_comment }}</div>
                            <div class="timeline-creator">
                              审核人：管理员
                            </div>
                          </div>
                        </div>

                        <!-- 总负责人分配 -->
                        <div v-if="feedback.specialist" class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">分配处理人</span>
                              <span class="timeline-time">{{ formatDate(feedback.updated_at) }}</span>
                            </div>
                            <div class="timeline-comment">
                              已分配给专项负责人：{{ feedback.specialist?.username || '未知用户' }}
                            </div>
                            <div class="timeline-creator">
                              分配人：总负责人
                            </div>
                          </div>
                        </div>

                        <!-- 专项负责人处理记录 -->
                        <div v-for="(record, index) in feedback.progress_records" 
                             :key="record.id" 
                             class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">{{ getProgressStatusText(record.progress_status) }}</span>
                              <span class="timeline-time">{{ formatDate(record.created_at) }}</span>
                            </div>
                            <div class="timeline-comment">{{ record.comment }}</div>
                            <div class="timeline-creator">
                              处理人：{{ record.created_by?.username || '未知用户' }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 公开反馈列表 -->
            <div v-if="activeTab === 'public'" class="feedback-list">
              <h4>公开反馈</h4>
              <div class="feedback-grid">
                <div v-for="feedback in publicFeedbacks" 
                     :key="feedback.id" 
                     :class="['feedback-card', { 'expanded': selectedFeedback?.id === feedback.id }]"
                     @click="toggleFeedbackDetail(feedback)">
                  <div class="card-header">
                    <h5>{{ feedback.title }}</h5>
                    <span :class="['status', feedback.status]">{{ getStatusText(feedback.status) }}</span>
                  </div>
                  <div class="card-content">
                    <p class="card-category">{{ getCategoryText(feedback.category) }}</p>
                    <p class="card-time">提交时间：{{ formatDate(feedback.created_at) }}</p>
                  </div>
                  <!-- 展开的详情内容 -->
                  <div v-if="selectedFeedback?.id === feedback.id" class="card-details">
                    <div class="detail-section">
                      <h4>基本信息</h4>
                      <p class="detail-content">{{ feedback.content }}</p>
                      <div class="detail-meta">
                        <span>类别：{{ getCategoryText(feedback.category) }}</span>
                        <span>状态：{{ getStatusText(feedback.status) }}</span>
                        <span>提交时间：{{ formatDate(feedback.created_at) }}</span>
                      </div>
                    </div>
                    
                    <div class="detail-section">
                      <h4>处理进度</h4>
                      <div class="progress-timeline">
                        <!-- 初始提交 -->
                        <div class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">提交反馈</span>
                              <span class="timeline-time">{{ formatDate(feedback.created_at) }}</span>
                            </div>
                            <div class="timeline-comment">{{ feedback.content }}</div>
                          </div>
                        </div>

                        <!-- 管理员审核 -->
                        <div v-if="feedback.admin_comment" class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">管理员审核</span>
                              <span class="timeline-time">{{ formatDate(feedback.updated_at) }}</span>
                            </div>
                            <div class="timeline-comment">{{ feedback.admin_comment }}</div>
                            <div class="timeline-creator">
                              审核人：管理员
                            </div>
                          </div>
                        </div>

                        <!-- 总负责人分配 -->
                        <div v-if="feedback.specialist" class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">分配处理人</span>
                              <span class="timeline-time">{{ formatDate(feedback.updated_at) }}</span>
                            </div>
                            <div class="timeline-comment">
                              已分配给专项负责人：{{ feedback.specialist?.username || '未知用户' }}
                            </div>
                            <div class="timeline-creator">
                              分配人：总负责人
                            </div>
                          </div>
                        </div>

                        <!-- 专项负责人处理记录 -->
                        <div v-for="(record, index) in feedback.progress_records" 
                             :key="record.id" 
                             class="timeline-item">
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <div class="timeline-header">
                              <span class="timeline-status">{{ getProgressStatusText(record.progress_status) }}</span>
                              <span class="timeline-time">{{ formatDate(record.created_at) }}</span>
                            </div>
                            <div class="timeline-comment">{{ record.comment }}</div>
                            <div class="timeline-creator">
                              处理人：{{ record.created_by?.username || '未知用户' }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 管理员界面 -->
          <div v-else-if="currentUser && currentUser.role === 'admin'">
            <!-- 用户管理 -->
            <div class="admin-section">
              <h4>用户管理</h4>
              <div class="user-list">
                <div v-for="user in users" :key="user.id" class="user-item">
                  <img :src="user.avatar" :alt="user.username" class="user-avatar">
                  <div class="user-info">
                    <div class="user-name">{{ user.username }}</div>
                    <div class="user-role">{{ getRoleText(user.role) }}</div>
                    <div class="user-created">注册时间：{{ formatDate(user.created_at) }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 反馈审核 -->
            <div class="admin-section">
              <h4>反馈审核</h4>
              <div class="feedback-grid">
                <div v-for="feedback in feedbacks" 
                     :key="feedback.id" 
                     :class="['feedback-card', `status-${feedback.status}`]">
                  <div class="card-header">
                    <h5>{{ feedback.title }}</h5>
                    <span :class="['status', feedback.status]">{{ getStatusText(feedback.status) }}</span>
                  </div>
                  <div class="card-content">
                    <div class="feedback-meta">
                      <div class="meta-item">
                        <span class="meta-label">提交者：</span>
                        <span class="meta-value">{{ feedback.student?.username || '未知用户' }}</span>
                      </div>
                      <div class="meta-item">
                        <span class="meta-label">类别：</span>
                        <span class="meta-value">{{ getCategoryText(feedback.category) }}</span>
                      </div>
                      <div class="meta-item">
                        <span class="meta-label">提交时间：</span>
                        <span class="meta-value">{{ formatDate(feedback.created_at) }}</span>
                      </div>
                    </div>
                    <p class="card-content-text">{{ feedback.content }}</p>
                  </div>
                  <div class="card-actions">
                    <button 
                      v-if="feedback.status === 'pending'"
                      class="action-button approve"
                      @click="handleApproveFeedback(feedback)"
                    >
                      通过审核
                    </button>
                    <button 
                      v-if="feedback.status === 'pending'"
                      class="action-button reject"
                      @click="handleRejectFeedback(feedback)"
                    >
                      驳回
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 总负责人界面 -->
          <div v-else-if="currentUser && currentUser.role === 'supervisor'" class="supervisor-interface">
            <div class="supervisor-section">
              <h4>待分配反馈</h4>
              <div class="feedback-grid">
                <div v-for="feedback in feedbacks.filter(f => !f.specialist_id)" 
                     :key="feedback.id" 
                     :class="['feedback-card', `status-${feedback.status}`]">
                  <div class="card-header">
                    <h5>{{ feedback.title }}</h5>
                    <span :class="['status', feedback.status]">{{ getStatusText(feedback.status) }}</span>
                  </div>
                  <div class="card-content">
                    <p class="card-category">{{ getCategoryText(feedback.category) }}</p>
                    <p class="card-time">提交时间：{{ formatDate(feedback.created_at) }}</p>
                    <p class="card-content-text">{{ feedback.content }}</p>
                  </div>
                  <div class="card-actions">
                    <div class="assign-section">
                      <select 
                        v-model="feedback.selectedSpecialist" 
                        class="specialist-select"
                      >
                        <option value="">选择专项负责人</option>
                        <option 
                          v-for="specialist in specialists" 
                          :key="specialist.id" 
                          :value="specialist.id"
                        >
                          {{ specialist.username }}
                        </option>
                      </select>
                      <button 
                        class="action-button assign"
                        @click="handleAssignFeedback(feedback)"
                        :disabled="!feedback.selectedSpecialist"
                      >
                        分配负责人
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 专项负责人界面 -->
          <div v-else-if="currentUser && currentUser.role === 'specialist'">
            <!-- 反馈列表 -->
            <div class="specialist-section">
              <h4>我的反馈</h4>
              <div class="feedback-list">
                <div v-for="feedback in feedbacks" :key="feedback.id" class="feedback-card specialist-feedback-card">
                  <!-- 基本信息卡片 -->
                  <div :class="['specialist-basic-info', feedback.status === 'completed' ? 'completed-info' : '']">
                    <div class="feedback-header">
                      <h5>{{ feedback.title }}</h5>
                      <span :class="['status', feedback.status]">{{ getStatusText(feedback.status) }}</span>
                    </div>
                    <div class="feedback-content">
                      <p class="feedback-desc">{{ feedback.content }}</p>
                      <div class="feedback-meta">
                        <span>提交者：{{ feedback.student.username }}</span>
                        <span>类别：{{ getCategoryText(feedback.category) }}</span>
                        <span>提交时间：{{ formatDate(feedback.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="feedback.admin_comment" class="admin-comment">
                    管理员审核意见：{{ feedback.admin_comment }}
                  </div>
                  <!-- 进度记录 -->
                  <div class="progress-records">
                    <h6 class="progress-title">处理进度</h6>
                    <div v-for="(record, index) in feedback.progress_records" :key="record.id" 
                         :class="['progress-item blue-progress-card', 
                                 (index === feedback.progress_records.length - 1 && record.progress_status === 'completed') ? 'completed-progress' : '']">
                      <div class="progress-header">
                        <span class="progress-status">{{ getProgressStatusText(record.progress_status) }}</span>
                        <span class="progress-time">{{ formatDate(record.created_at) }}</span>
                      </div>
                      <div class="progress-comment">{{ record.comment }}</div>
                    </div>
                  </div>
                  <!-- 更新进度 -->
                  <div v-if="feedback.status !== 'completed'" class="progress-actions">
                    <textarea v-model="feedback.newProgressComment" 
                             placeholder="请输入进度说明"
                             class="progress-input"></textarea>
                    <div class="progress-buttons">
                      <button @click="handleUpdateProgress(feedback, 'processing')" 
                              class="continue-btn">
                        继续进行
                      </button>
                      <button @click="handleUpdateProgress(feedback, 'completed')" 
                              class="complete-btn">
                        已结束
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 添加相似反馈模态框 -->
        <div class="modal" v-if="showSimilarModal">
          <div class="modal-content">
            <h3>发现相似反馈</h3>
            <p>系统发现以下反馈与您要提交的内容相似：</p>
            <div class="similar-feedback">
              <h4>{{ similarFeedback.title }}</h4>
              <p class="feedback-content">{{ similarFeedback.content }}</p>
              <p class="feedback-category">类别：{{ similarFeedback.category }}</p>
              <p class="feedback-time">提交时间：{{ formatDate(similarFeedback.created_at) }}</p>
            </div>
            <p>您是否仍要提交新的反馈？</p>
            <div class="modal-buttons">
              <button @click="confirmSubmit">继续提交</button>
              <button @click="cancelSubmit">取消提交</button>
            </div>
          </div>
        </div>

        <!-- 添加加载状态模态框 -->
        <div class="modal" v-if="isCheckingSimilar">
          <div class="modal-content loading-modal">
            <div class="loading-spinner"></div>
            <h3>正在检测相似反馈</h3>
            <p>请稍候，系统正在检查是否有类似的反馈...</p>
          </div>
        </div>

        <!-- 管理员评论对话框 -->
        <div v-if="showCommentDialog" class="modal-overlay">
          <div class="modal-content">
            <h3>{{ reviewAction === 'approve' ? '通过审核' : '驳回反馈' }}</h3>
            <div class="form-group">
              <label>审核意见：</label>
              <textarea
                v-model="reviewComment"
                class="form-input"
                rows="4"
                placeholder="请输入审核意见..."
              ></textarea>
            </div>
            <div class="modal-actions">
              <button class="action-button cancel" @click="showCommentDialog = false">取消</button>
              <button 
                class="action-button submit" 
                :class="{ 'approve': reviewAction === 'approve', 'reject': reviewAction === 'reject' }"
                @click="submitReview"
              >
                确认{{ reviewAction === 'approve' ? '通过' : '驳回' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { login, register, getStudentFeedbacks, submitFeedback, getAllUsers, getAllFeedbacks, reviewFeedback, getSupervisorFeedbacks, assignFeedback, getSpecialistFeedbacks, updateFeedbackProgress, getPublicFeedbacks, toggleFeedbackPublic, checkSimilarFeedback } from './api'

const users = ref([])
const loginName = ref('')
const loginPassword = ref('')
const currentUser = ref(null)
const loginError = ref('')

const showRegister = ref(false)
const registerData = ref({
  username: '',
  password: '',
  confirmPassword: '',
  role: 'student'
})
const registerError = ref('')
const registerSuccess = ref('')

const feedbacks = ref([])
const newFeedback = ref({
  title: '',
  category: '',
  content: ''
})

const selectedCategory = ref('')
const specialists = ref([])
const selectedFeedback = ref(null)
const activeTab = ref('submit')
const publicFeedbacks = ref([])

// 添加相似反馈相关的状态
const showSimilarModal = ref(false)
const similarFeedback = ref(null)
const pendingFeedback = ref(null)
const isCheckingSimilar = ref(false)

// 背景图片相关的状态
const backgroundImage = ref('')
const backgroundImages = ['1.jpg', '2.jpg', '3.jpg']

// 在 script setup 部分添加新的响应式变量
const showCommentDialog = ref(false);
const reviewComment = ref('');
const currentFeedback = ref(null);
const reviewAction = ref(''); // 'approve' 或 'reject'

onMounted(async () => {
  const res = await getAllUsers()
  users.value = res.data
  backgroundImage.value = getRandomBackground()
  await loadSupervisorData()
})

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

// 获取类别文本
const getCategoryText = (category) => {
  const categoryMap = {
    'academic': '学术问题',
    'facility': '设施问题',
    'service': '服务问题',
    'other': '其他问题'
  }
  return categoryMap[category] || category
}

// 格式化日期
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

// 加载学生反馈列表
const loadFeedbacks = async () => {
  if (currentUser.value?.role === 'student') {
    try {
      const response = await getStudentFeedbacks(currentUser.value.id)
      feedbacks.value = response.data
    } catch (error) {
      console.error('加载反馈列表失败:', error)
      alert('加载反馈列表失败，请稍后重试')
    }
  }
}

// 提交新反馈
const handleSubmitFeedback = async () => {
  try {
    if (!newFeedback.value.title || !newFeedback.value.category || !newFeedback.value.content) {
      alert('请填写完整信息')
      return
    }

    // 保存当前表单数据
    pendingFeedback.value = {
      title: newFeedback.value.title,
      content: newFeedback.value.content,
      category: newFeedback.value.category
    }

    // 显示加载状态
    isCheckingSimilar.value = true

    try {
      // 检查相似反馈
      const checkResult = await checkSimilarFeedback({
        title: newFeedback.value.title,
        content: newFeedback.value.content,
        category: newFeedback.value.category,
        student_id: currentUser.value.id
      })

      // 隐藏加载状态
      isCheckingSimilar.value = false

      if (checkResult.data.similar) {
        // 显示相似反馈模态框
        similarFeedback.value = checkResult.data.similar_feedback
        showSimilarModal.value = true
      } else {
        // 直接提交反馈
        const feedbackData = {
          ...pendingFeedback.value,
          student_id: currentUser.value.id
        }
        await submitFeedback(feedbackData)
        
        // 清空表单
        newFeedback.value = {
          title: '',
          content: '',
          category: ''
        }
        pendingFeedback.value = null
        
        // 重新加载反馈列表
        await loadFeedbacks()
        alert('反馈提交成功')
      }
    } catch (error) {
      // 确保在出错时也隐藏加载状态
      isCheckingSimilar.value = false
      throw error
    }
  } catch (error) {
    console.error('提交反馈失败:', error)
    alert('提交反馈失败，请稍后重试')
  }
}

// 获取角色文本
const getRoleText = (role) => {
  const roleMap = {
    'student': '学生',
    'admin': '管理员',
    'supervisor': '总负责人',
    'specialist': '专项负责人'
  }
  return roleMap[role] || role
}

// 加载管理员数据
const loadAdminData = async () => {
  try {
    const [usersRes, feedbacksRes] = await Promise.all([
      getAllUsers(),
      getAllFeedbacks()
    ])
    users.value = usersRes.data
    feedbacks.value = feedbacksRes.data
  } catch (error) {
    console.error('Error loading admin data:', error)
    alert('加载数据失败，请刷新页面重试')
  }
}

// 审核反馈
const handleReviewFeedback = async (feedback, status) => {
  try {
    await reviewFeedback(feedback.id, {
      status,
      comment: feedback.reviewComment || ''
    })
    
    // 更新本地数据
    feedback.status = status
    feedback.admin_comment = feedback.reviewComment
    feedback.reviewComment = ''
    
    alert('审核完成')
  } catch (error) {
    alert(error.response?.data?.error || '审核失败，请重试')
  }
}

// 过滤反馈列表
const filteredFeedbacks = computed(() => {
  if (!selectedCategory.value) {
    return feedbacks.value
  }
  return feedbacks.value.filter(f => f.category === selectedCategory.value)
})

// 加载总负责人数据
const loadSupervisorData = async () => {
  try {
    // 获取所有反馈
    const feedbacksResponse = await getSupervisorFeedbacks();
    // 为每条反馈添加 selectedSpecialist 字段
    feedbacks.value = feedbacksResponse.data.map(fb => ({
      ...fb,
      selectedSpecialist: ''
    }));
    // 获取所有专项负责人
    const usersResponse = await getAllUsers();
    specialists.value = usersResponse.data.filter(user => user.role === 'specialist');
  } catch (error) {
    console.error('加载总负责人数据失败:', error);
    alert('加载数据失败，请刷新页面重试');
  }
};

// 修改分配反馈的处理函数
const handleAssignFeedback = async (feedback) => {
  if (!feedback.selectedSpecialist) {
    alert('请选择专项负责人');
    return;
  }

  try {
    await assignFeedback(feedback.id, {
      specialist_id: feedback.selectedSpecialist
    });
    alert('分配成功');
    // 分配成功后，重新加载待分配反馈列表
    await loadSupervisorData();
  } catch (error) {
    console.error('Error assigning feedback:', error);
    if (error.response?.status === 400) {
      alert(error.response.data.error || '专项负责人ID不能为空');
    } else if (error.response?.status === 403) {
      alert('无权操作此反馈');
    } else {
      alert('分配失败，请稍后重试');
    }
  }
};

// 获取进度状态文本
const getProgressStatusText = (status) => {
  const statusMap = {
    'processing': '处理中',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

// 加载专项负责人数据
const loadSpecialistData = async () => {
  try {
    const response = await getSpecialistFeedbacks(currentUser.value.id)
    feedbacks.value = response.data
  } catch (error) {
    console.error('加载专项负责人数据失败:', error)
  }
}

// 更新反馈进度
const handleUpdateProgress = async (feedback, progressStatus) => {
  if (!feedback.newProgressComment) {
    alert('请输入进度说明')
    return
  }
  
  try {
    await updateFeedbackProgress(feedback.id, {
      progress_status: progressStatus,
      comment: feedback.newProgressComment,
      specialist_id: currentUser.value.id
    })
    
    // 更新本地数据
    feedback.progress_records.push({
      progress_status: progressStatus,
      comment: feedback.newProgressComment,
      created_at: new Date().toISOString(),
      created_by: {
        id: currentUser.value.id,
        username: currentUser.value.username,
        avatar: currentUser.value.avatar
      }
    })
    
    if (progressStatus === 'completed') {
      feedback.status = 'completed'
    }
    
    feedback.newProgressComment = ''
    alert('进度更新成功')
  } catch (error) {
    alert(error.response?.data?.error || '更新失败，请重试')
  }
}

const handleLogin = async () => {
  try {
    const response = await login(loginName.value, loginPassword.value)
    currentUser.value = response.data
    loginError.value = ''
    
    // 根据用户角色加载相应的数据
    if (currentUser.value.role === 'student') {
      await loadFeedbacks()
    } else if (currentUser.value.role === 'admin') {
      await loadAdminData()
    } else if (currentUser.value.role === 'supervisor') {
      await loadSupervisorData()
    } else if (currentUser.value.role === 'specialist') {
      await loadSpecialistData()
    }
  } catch (error) {
    loginError.value = error.response?.data?.error || '登录失败，请重试'
  }
}

const handleRegister = async () => {
  if (registerData.value.password !== registerData.value.confirmPassword) {
    registerError.value = '两次输入的密码不一致'
    return
  }

  try {
    const response = await register({
      username: registerData.value.username,
      password: registerData.value.password,
      role: registerData.value.role
    })
    currentUser.value = response.data
    registerError.value = ''
    registerSuccess.value = '注册成功！'
    showRegister.value = false
  } catch (error) {
    registerError.value = error.response?.data?.error || '注册失败，请重试'
  }
}

const handleLogout = () => {
  currentUser.value = null
  loginName.value = ''
  loginPassword.value = ''
  loginError.value = ''
  feedbacks.value = []
}

// 切换反馈详情显示
const toggleFeedbackDetail = (feedback) => {
  if (selectedFeedback.value?.id === feedback.id) {
    selectedFeedback.value = null
  } else {
    selectedFeedback.value = {
      ...feedback,
      student: feedback.student || { username: '未知用户' },
      specialist: feedback.specialist || null,
      progress_records: feedback.progress_records || [],
      admin_comment: feedback.admin_comment || null
    }
  }
}

// 加载公开反馈列表
const loadPublicFeedbacks = async () => {
  try {
    console.log('Loading public feedbacks...');
    const response = await getPublicFeedbacks();
    console.log('Public feedbacks response:', response);
    
    if (response.data) {
      publicFeedbacks.value = response.data;
      console.log('Updated public feedbacks list:', publicFeedbacks.value);
    } else {
      console.warn('No data in public feedbacks response');
      publicFeedbacks.value = [];
    }
  } catch (error) {
    console.error('加载公开反馈失败:', error);
    if (error.response) {
      console.error('Error response:', error.response.data);
    }
    alert('加载公开反馈失败，请稍后重试');
    publicFeedbacks.value = [];
  }
};

// 处理公开状态切换
const handleTogglePublic = async (feedback) => {
  try {
    // 发送请求，包含 student_id
    await toggleFeedbackPublic(feedback.id, {
      is_public: !feedback.is_public,
      student_id: currentUser.value.id
    });
    
    // 更新本地状态
    feedback.is_public = !feedback.is_public;
    // 显示成功提示
    alert(feedback.is_public ? '反馈已设为公开' : '反馈已设为私密');
    
    // 如果设置为公开，刷新公开反馈列表
    if (feedback.is_public) {
      await loadPublicFeedbacks();
    }
  } catch (error) {
    console.error('Error toggling public status:', error);
    if (error.response?.status === 403) {
      alert('您没有权限修改此反馈的公开状态');
    } else {
      alert('操作失败，请稍后重试');
    }
  }
};

// 监听标签页切换
watch(activeTab, (newTab) => {
  if (newTab === 'public') {
    loadPublicFeedbacks()
  }
})

// 确认提交
const confirmSubmit = async () => {
  try {
    showSimilarModal.value = false
    // 使用pendingFeedback中的数据
    const feedbackData = {
      title: pendingFeedback.value.title,
      content: pendingFeedback.value.content,
      category: pendingFeedback.value.category,
      student_id: currentUser.value.id
    }
    await submitFeedback(feedbackData)
    
    // 清空表单和临时数据
    newFeedback.value = {
      title: '',
      content: '',
      category: ''
    }
    pendingFeedback.value = null
    similarFeedback.value = null
    
    // 重新加载反馈列表
    await loadFeedbacks()
    alert('反馈提交成功')
  } catch (error) {
    console.error('提交反馈失败:', error)
    alert('提交反馈失败，请稍后重试')
  }
}

// 取消提交
const cancelSubmit = () => {
  showSimilarModal.value = false
  similarFeedback.value = null
  pendingFeedback.value = null
  // 清空表单
  newFeedback.value = {
    title: '',
    content: '',
    category: ''
  }
}

// 随机选择背景图片
const getRandomBackground = () => {
  const randomIndex = Math.floor(Math.random() * backgroundImages.length)
  return `/pic/${backgroundImages[randomIndex]}`
}

// 计算背景样式
const backgroundStyle = computed(() => ({
  backgroundImage: `url(${backgroundImage.value})`
}))

// 获取角色标题
const getRoleTitle = (role) => {
  const titleMap = {
    'student': '学生反馈中心',
    'admin': '管理员控制台',
    'supervisor': '总负责人控制台',
    'specialist': '专项负责人控制台'
  }
  return titleMap[role] || role
}

// 显示评论对话框
const showReviewDialog = (feedback, action) => {
  currentFeedback.value = feedback;
  reviewAction.value = action;
  reviewComment.value = '';
  showCommentDialog.value = true;
};

// 提交审核结果
const submitReview = async () => {
  if (!reviewComment.value.trim()) {
    alert('请输入审核意见');
    return;
  }

  try {
    await reviewFeedback(currentFeedback.value.id, {
      status: reviewAction.value === 'approve' ? 'processing' : 'rejected',
      comment: reviewComment.value
    });
    
    // 刷新反馈列表
    await loadSupervisorData();
    alert(reviewAction.value === 'approve' ? '反馈已通过审核' : '反馈已驳回');
    
    // 关闭对话框
    showCommentDialog.value = false;
    reviewComment.value = '';
    currentFeedback.value = null;
  } catch (error) {
    console.error('Error reviewing feedback:', error);
    alert('操作失败，请稍后重试');
  }
};

// 修改管理员界面的按钮点击事件
const handleApproveFeedback = (feedback) => {
  showReviewDialog(feedback, 'approve');
};

const handleRejectFeedback = (feedback) => {
  showReviewDialog(feedback, 'reject');
};
</script>

<style scoped>
/* 全局样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f7fa;
}

/* 容器样式 */
.app-container {
  min-height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.app-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 0;
}

.content-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 登录和注册表单样式 */
.login-form, .register-form {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 40%;
  min-width: 400px;
  margin: 0 auto;
}

.login-form h4, .register-form h3 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
  font-size: 28px;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  color: #2c3e50;
  font-weight: 500;
  font-size: 16px;
}

.form-input {
  width: 100%;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-input::placeholder {
  color: #a0aec0;
}

.login-btn, .register-btn, .cancel-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 10px;
}

.login-btn {
  background-color: #3498db;
  color: white;
}

.login-btn:hover {
  background-color: #2980b9;
}

.register-btn {
  background-color: #2ecc71;
  color: white;
}

.register-btn:hover {
  background-color: #27ae60;
}

.cancel-btn {
  background-color: #e74c3c;
  color: white;
}

.cancel-btn:hover {
  background-color: #c0392b;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 15px;
  text-align: center;
}

.success-message {
  color: #2ecc71;
  margin-bottom: 15px;
  text-align: center;
}

/* 导航栏样式 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: white;
  padding: 15px 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 30px;
}

.navbar-title-bg {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.role-title {
  font-size: 22px;
  font-weight: 500;
  color: #000;
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  color: #2c3e50;
  font-size: 18px;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 16px;
}

.logout-btn:hover {
  background-color: #c0392b;
}

/* 其他现有样式保持不变 */
/* 调整现有容器样式以适应新背景 */
.container {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(4px);
}

/* 调整卡片样式以适应新背景 */
.feedback-card {
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(4px);
}

/* 调整模态框样式以适应新背景 */
.modal-content {
  background-color: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(8px);
}

/* 标题样式 */
h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2.5em;
  font-weight: 600;
}

/* 导航标签样式 */
.nav-tabs {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  border-bottom: 2px solid #e0e6ed;
  padding-bottom: 10px;
}

.nav-tab {
  padding: 10px 20px;
  cursor: pointer;
  color: #606f7b;
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 6px;
}

.nav-tab:hover {
  color: #3498db;
  background-color: #f8fafc;
}

.nav-tab.active {
  color: #3498db;
  background-color: #ebf8ff;
  border-bottom: 2px solid #3498db;
}

/* 表单样式 */
.feedback-form {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #4a5568;
  font-weight: 500;
}

.form-group textarea {
  min-height: 120px;
  resize: vertical;
}

/* 按钮样式 */
button {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

button:active {
  transform: translateY(0);
}

.submit-btn {
  background-color: #3498db;
  color: white;
  width: 100%;
}

.submit-btn:hover {
  background-color: #2980b9;
}

/* 反馈卡片样式 */
.feedback-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.feedback-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.feedback-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.feedback-card.expanded {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h5 {
  font-size: 18px;
  color: #2c3e50;
  margin: 0;
}

.card-content {
  color: #64748b;
}

.card-category {
  margin-bottom: 8px;
}

.card-time {
  font-size: 14px;
  color: #94a3b8;
}

/* 展开的详情样式 */
.card-details {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h4 {
  font-size: 18px;
  color: #2c3e50;
  margin-bottom: 15px;
}

.detail-content {
  font-size: 16px;
  line-height: 1.6;
  color: #4a5568;
  margin-bottom: 15px;
}

.detail-meta {
  display: flex;
  gap: 20px;
  color: #64748b;
  font-size: 14px;
}

/* 进度时间线样式 */
.progress-timeline {
  position: relative;
  padding-left: 20px;
  margin-top: 20px;
}

.timeline-item {
  position: relative;
  padding-bottom: 25px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: -14px;
  top: 12px;
  bottom: -12px;
  width: 2px;
  background: #e2e8f0;
}

.timeline-marker {
  position: absolute;
  left: -20px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #3498db;
  border: 2px solid white;
  box-shadow: 0 0 0 2px #3498db;
  z-index: 1;
}

.timeline-content {
  background: #f8fafc;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.timeline-content:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.timeline-status {
  font-weight: 500;
  color: #2c3e50;
  font-size: 15px;
}

.timeline-time {
  color: #64748b;
  font-size: 14px;
}

.timeline-comment {
  color: #4a5568;
  margin-bottom: 8px;
  line-height: 1.5;
  font-size: 15px;
}

.timeline-creator {
  font-size: 14px;
  color: #64748b;
  font-style: italic;
}

/* 不同状态的时间线标记颜色 */
.timeline-item:nth-child(1) .timeline-marker {
  background: #3498db;
  box-shadow: 0 0 0 2px #3498db;
}

.timeline-item:nth-child(2) .timeline-marker {
  background: #2ecc71;
  box-shadow: 0 0 0 2px #2ecc71;
}

.timeline-item:nth-child(3) .timeline-marker {
  background: #f1c40f;
  box-shadow: 0 0 0 2px #f1c40f;
}

.timeline-item:nth-child(4) .timeline-marker {
  background: #e74c3c;
  box-shadow: 0 0 0 2px #e74c3c;
}

/* 展开卡片时的动画效果 */
.feedback-card.expanded {
  transform: scale(1.02);
  transition: transform 0.3s ease;
}

.card-details {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 状态标签样式 */
.status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.status.pending {
  background: #fef3c7;
  color: #92400e;
}

.status.processing {
  background: #dbeafe;
  color: #1e40af;
}

.status.completed {
  background: #dcfce7;
  color: #166534;
}

.status.rejected {
  background: #fee2e2;
  color: #991b1b;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.5em;
}

.similar-feedback {
  background-color: #f8fafc;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  border: 1px solid #e2e8f0;
}

.similar-feedback h4 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.modal-buttons {
    display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
}

.modal-buttons button {
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.modal-buttons button:first-child {
  background-color: #3498db;
  color: white;
}

.modal-buttons button:last-child {
  background-color: #e53e3e;
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }

  .nav-tabs {
    flex-direction: column;
    gap: 10px;
  }

  .feedback-list {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    padding: 20px;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feedback-card {
  animation: fadeIn 0.3s ease-out;
}

/* 加载状态 */
.loading {
  text-align: center;
  padding: 20px;
  color: #718096;
}

/* 顶部导航栏样式 */
.navbar-title-bg {
  background: #fff;
  color: #3498db;
  font-weight: bold;
  font-size: 1.5em;
  padding: 8px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  letter-spacing: 4px;
}

/* 让内容不被导航栏遮挡 */
.app-container, .content-wrapper {
  margin-top: 64px;
}

/* 内容区域样式 */
.content-wrapper {
  padding-top: 80px;
}

.nav-tabs {
  margin-bottom: 30px;
}

.nav-tab {
  font-size: 18px;
  padding: 12px 24px;
}

.feedback-form h4,
.feedback-list h4 {
  font-size: 22px;
  margin-bottom: 20px;
}

.form-group label {
  font-size: 18px;
}

.form-input {
  font-size: 18px;
  padding: 14px;
}

/* 管理员界面样式 */
.admin-section {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.user-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.user-item:hover {
  transform: translateY(-2px);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 15px;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 18px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.user-role {
  font-size: 16px;
  color: #64748b;
  margin-bottom: 4px;
}

.user-created {
  font-size: 14px;
  color: #94a3b8;
}

/* 管理员界面反馈卡片状态样式 */
.feedback-card.status-pending {
  background: #f8fafc;
  border-left: 4px solid #94a3b8;
}

.feedback-card.status-processing {
  background: #eff6ff;
  border-left: 4px solid #3b82f6;
}

.feedback-card.status-completed {
  background: #f0fdf4;
  border-left: 4px solid #22c55e;
}

.feedback-card.status-rejected {
  background: #fef2f2;
  border-left: 4px solid #ef4444;
}

.card-content-text {
  margin-top: 12px;
  color: #4a5568;
  line-height: 1.6;
}

.card-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.action-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.action-button.approve {
  background: #22c55e;
  color: white;
}

.action-button.approve:hover {
  background: #16a34a;
}

.action-button.reject {
  background: #ef4444;
  color: white;
}

.action-button.reject:hover {
  background: #dc2626;
}

/* 总负责人界面反馈卡片类别样式 */
.feedback-card.category-academic {
  background: #f0f9ff;
  border-left: 4px solid #0ea5e9;
}

.feedback-card.category-facility {
  background: #f0fdf4;
  border-left: 4px solid #22c55e;
}

.feedback-card.category-service {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
}

.feedback-card.category-other {
  background: #f3f4f6;
  border-left: 4px solid #6b7280;
}

.admin-comment {
  margin-top: 12px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  border-left: 3px solid #3b82f6;
}

.comment-label {
  font-weight: 500;
  color: #1e40af;
}

.comment-content {
  color: #4a5568;
  margin-left: 8px;
}

.action-button.assign {
  background: #3b82f6;
  color: white;
}

.action-button.assign:hover {
  background: #2563eb;
}

/* 状态组样式 */
.status-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* 公开状态标签样式 */
.public-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  background: #f1f5f9;
  color: #64748b;
}

.public-status.is-public {
  background: #dbeafe;
  color: #1e40af;
}

/* 公开选项样式 */
.public-option {
  margin-top: 12px;
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.public-option:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.public-option label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4a5568;
  cursor: pointer;
  user-select: none;
}

.public-option input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #3b82f6;
}

.public-option input[type="checkbox"]:checked + span {
  color: #1e40af;
}

/* 评论对话框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #2c3e50;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.modal-actions button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
}

.modal-actions .cancel {
  background: #e2e8f0;
  color: #64748b;
}

.modal-actions .cancel:hover {
  background: #cbd5e1;
}

.modal-actions .submit {
  color: white;
}

.modal-actions .submit.approve {
  background: #3b82f6;
}

.modal-actions .submit.approve:hover {
  background: #2563eb;
}

.modal-actions .submit.reject {
  background: #ef4444;
}

.modal-actions .submit.reject:hover {
  background: #dc2626;
}

/* 分配部分样式 */
.assign-section {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-top: 15px;
}

.specialist-select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 16px;
  color: #4a5568;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.specialist-select:hover {
  border-color: #cbd5e1;
}

.specialist-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.specialist-select:disabled {
  background-color: #f1f5f9;
  cursor: not-allowed;
}

.action-button.assign {
  background: #3b82f6;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
}

.action-button.assign:hover {
  background: #2563eb;
}

.action-button.assign:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

/* 在 style 区域添加专项负责人卡片样式 */
.specialist-feedback-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.10);
  padding: 20px;
  margin-bottom: 20px;
  transition: box-shadow 0.3s;
}
.specialist-feedback-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

/* style: 添加专项负责人基本信息卡片样式 */
.specialist-basic-info {
  background: rgba(205, 170, 125, 0.18); /* 浅棕色半透明 */
  border-radius: 10px;
  padding: 18px 20px 12px 20px;
  margin-bottom: 18px;
  box-shadow: 0 1px 4px rgba(205, 170, 125, 0.10);
}
.specialist-basic-info .feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.specialist-basic-info h5 {
  font-size: 20px;
  color: #7c5a2a;
  margin: 0;
}
.specialist-basic-info .status {
  font-size: 15px;
}
.specialist-basic-info .feedback-desc {
  color: #6b4c1b;
  font-size: 16px;
  margin-bottom: 10px;
}
.specialist-basic-info .feedback-meta {
  display: flex;
  gap: 18px;
  color: #8d6a3a;
  font-size: 14px;
}

/* style: 进度标题和蓝色卡片样式 */
.progress-title {
  font-size: 20px;
  font-weight: bold;
  color: #2563eb;
  margin-bottom: 14px;
}
.blue-progress-card {
  background: rgba(37, 99, 235, 0.10); /* 浅蓝色半透明 */
  border-radius: 8px;
  padding: 14px 16px 10px 16px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(37, 99, 235, 0.08);
}

/* style: 添加已完成反馈的样式 */
.completed-info {
  background: rgba(34, 197, 94, 0.18); /* 浅绿色半透明 */
  box-shadow: 0 1px 4px rgba(34, 197, 94, 0.10);
}
.completed-info h5 {
  color: #166534;
}
.completed-info .feedback-desc {
  color: #166534;
}
.completed-info .feedback-meta {
  color: #166534;
}
.completed-progress {
  background: rgba(34, 197, 94, 0.10); /* 浅绿色半透明 */
  box-shadow: 0 1px 4px rgba(34, 197, 94, 0.08);
}

/* 加载状态模态框样式 */
.loading-modal {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-modal h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.loading-modal p {
  color: #666;
  font-size: 16px;
}

/* 反馈元信息样式 */
.feedback-meta {
  margin-bottom: 15px;
  padding: 10px;
  background: #f8fafc;
  border-radius: 6px;
}

.meta-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.meta-item:last-child {
  margin-bottom: 0;
}

.meta-label {
  font-weight: 500;
  color: #64748b;
  min-width: 80px;
}

.meta-value {
  color: #1e293b;
}

.card-content-text {
  margin-top: 15px;
  color: #4a5568;
  line-height: 1.6;
  white-space: pre-wrap;
}
</style>
