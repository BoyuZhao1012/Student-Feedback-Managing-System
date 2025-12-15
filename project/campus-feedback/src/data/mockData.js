// 模拟用户数据
export const users = [
  {
    id: 1,
    name: '张三',
    role: 'student',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  },
  {
    id: 2,
    name: '李四',
    role: 'admin',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  },
  {
    id: 3,
    name: '王五',
    role: 'supervisor',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  },
  {
    id: 4,
    name: '赵六',
    role: 'specialist',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  }
];

// 模拟反馈数据
export const feedbacks = [
  {
    id: 1,
    title: '图书馆空调温度过高',
    content: '图书馆二楼的空调温度设置过高，导致学习环境不舒适。',
    category: '设施',
    status: 'pending',
    created_at: '2024-03-15 10:00:00',
    student_id: 1,
    assigned_to: null,
    is_public: true,
    progress: []
  },
  {
    id: 2,
    title: '食堂卫生问题',
    content: '食堂后厨卫生状况需要改善。',
    category: '生活',
    status: 'in_progress',
    created_at: '2024-03-14 15:30:00',
    student_id: 1,
    specialist_id: 4,
    is_public: true,
    progress: [
      {
        content: '已安排检查',
        created_at: '2024-03-14 16:00:00',
        user_id: 4
      }
    ]
  },
  {
    id: 3,
    title: '教学楼灯光问题',
    content: '教学楼走廊灯光昏暗，影响学生安全。',
    category: '设施',
    status: 'completed',
    created_at: '2024-03-13 09:00:00',
    student_id: 1,
    specialist_id: 4,
    is_public: true,
    progress: [
      {
        content: '已安排维修',
        created_at: '2024-03-13 10:00:00',
        user_id: 4
      },
      {
        content: '维修完成',
        created_at: '2024-03-13 15:00:00',
        user_id: 4
      }
    ]
  }
];

// 模拟分类数据
export const categories = [
  { value: '设施', label: '校园设施' },
  { value: '教学', label: '教学相关' },
  { value: '生活', label: '生活服务' },
  { value: '安全', label: '校园安全' },
  { value: '其他', label: '其他' }
];

// 模拟状态数据
export const statuses = [
  { value: 'pending', label: '待处理' },
  { value: 'in_progress', label: '处理中' },
  { value: 'completed', label: '已完成' },
  { value: 'rejected', label: '已拒绝' }
]; 