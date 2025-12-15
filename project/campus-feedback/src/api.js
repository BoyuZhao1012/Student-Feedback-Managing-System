import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 登录
export const login = (username, password) => api.post('/login', { username, password });

// 注册
export const register = (data) => api.post('/register', data);

// 获取所有用户
export const getAllUsers = () => api.get('/admin/users');

// 获取所有反馈
export const getAllFeedbacks = () => api.get('/admin/feedbacks');

// 审核反馈
export const reviewFeedback = (feedbackId, data) => api.post(`/admin/feedbacks/${feedbackId}/review`, data);

// 获取学生反馈列表
export const getStudentFeedbacks = (studentId) => api.get(`/student/feedbacks?student_id=${studentId}`);

// 提交反馈
export const submitFeedback = (data) => api.post('/student/feedbacks', data);

// 获取反馈列表
export const getFeedbacks = (params) => api.get('/feedbacks', { params });

// 新建反馈
export const createFeedback = (data) => api.post('/feedbacks', data);

// 更新反馈
export const updateFeedback = (id, data) => api.put(`/feedbacks/${id}`, data);

// 添加进度
export const addProgress = (feedbackId, data) => api.post(`/feedbacks/${feedbackId}/progress`, data);

// 总负责人相关API
export const getSupervisorFeedbacks = () => api.get('/supervisor/feedbacks');

// 分配反馈
export const assignFeedback = (feedbackId, data) => api.post(`/supervisor/feedbacks/${feedbackId}/assign`, data);

// 专项负责人相关API
export const getSpecialistFeedbacks = (specialistId) => api.get(`/specialist/feedbacks?specialist_id=${specialistId}`);

// 更新反馈进度
export const updateFeedbackProgress = (feedbackId, data) => api.post(`/specialist/feedbacks/${feedbackId}/progress`, data);

// 公开反馈相关
export const getPublicFeedbacks = () => api.get('/public/feedbacks');
export const toggleFeedbackPublic = (feedbackId, data) => api.post(`/student/feedbacks/${feedbackId}/public`, data);

// 检查相似反馈
export const checkSimilarFeedback = (data) => api.post('/student/feedbacks/check-similar', data)

export default api; 