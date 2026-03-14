/**
 * Demo Skill - Greeting Implementation
 * 
 * 演示技能的 TypeScript 实现
 * 用于展示如何在 Skill 目录中包含代码实现
 */

// 问候上下文接口
interface GreetingContext {
  name: string;
  language?: 'zh' | 'en';
  style?: 'friendly' | 'formal';
}

// 问候结果接口
interface GreetingResult {
  success: boolean;
  greeting: string;
  input: {
    name: string;
    language: string;
    style: string;
  };
}

// 问候模板
const GREETING_TEMPLATES = {
  zh: {
    friendly: [
      '你好，{name}！👋 很高兴见到你！',
      '嗨，{name}！👋 欢迎使用 SuperClaude 框架！',
      '{name}，你好呀！👋 希望你今天过得愉快！',
    ],
    formal: [
      '您好，{name}。欢迎使用 SuperClaude 框架。',
      '尊敬的 {name}，感谢您使用本系统。',
      '{name}，您好。很荣幸为您服务。',
    ],
  },
  en: {
    friendly: [
      'Hello, {name}! 👋 Great to see you!',
      'Hi {name}! 👋 Welcome to SuperClaude framework!',
      'Hey {name}! 👋 Hope you have a wonderful day!',
    ],
    formal: [
      'Good day, {name}. Welcome to the SuperClaude framework.',
      'Greetings, {name}. Thank you for using our system.',
      'Dear {name}, it is our pleasure to serve you.',
    ],
  },
};

/**
 * 生成问候语
 * 
 * @param context - 问候上下文，包含名称、语言和风格
 * @returns 问候结果
 * 
 * @example
 * ```typescript
 * const result = generateGreeting({
 *   name: '小明',
 *   language: 'zh',
 *   style: 'friendly'
 * });
 * console.log(result.greeting);
 * // 输出: 你好，小明！👋 很高兴见到你！
 * ```
 */
export function generateGreeting(context: GreetingContext): GreetingResult {
  const { name, language = 'zh', style = 'friendly' } = context;

  // 参数验证
  if (!name || name.trim() === '') {
    return {
      success: false,
      greeting: '❌ 错误: 缺少必需参数 "name"',
      input: {
        name: '(未提供)',
        language,
        style,
      },
    };
  }

  // 获取模板
  const templates = GREETING_TEMPLATES[language]?.[style];
  if (!templates) {
    return {
      success: false,
      greeting: `❌ 错误: 不支持的语言(${language})或风格(${style})`,
      input: {
        name,
        language,
        style,
      },
    };
  }

  // 随机选择模板
  const template = templates[Math.floor(Math.random() * templates.length)];
  const greeting = template.replace('{name}', name);

  return {
    success: true,
    greeting,
    input: {
      name,
      language,
      style,
    },
  };
}

/**
 * 格式化输出
 * 
 * @param result - 问候结果
 * @returns 格式化的输出字符串
 */
export function formatOutput(result: GreetingResult): string {
  const { success, greeting, input } = result;

  if (success) {
    return `
🎉 Demo Skill 响应

📝 输入:
   - 名称: ${input.name}
   - 语言: ${input.language}
   - 风格: ${input.style}

💬 问候:
   ${greeting}

✅ 状态: 技能执行成功
`.trim();
  } else {
    return `
❌ Demo Skill 错误

📝 输入:
   - 名称: ${input.name}
   - 语言: ${input.language}
   - 风格: ${input.style}

⚠️ ${greeting}

💡 建议: 请检查输入参数
`.trim();
  }
}

/**
 * 检查技能状态
 * 
 * @returns 状态信息
 */
export function checkStatus(): string {
  return `
🔍 Demo Skill 状态检查

📊 运行信息:
   - 版本: 1.0.0
   - 状态: ✅ 正常运行
   - 支持语言: zh, en
   - 支持风格: friendly, formal

✅ 技能配置正确，可以正常使用
`.trim();
}

// 导出默认函数
export default generateGreeting;

