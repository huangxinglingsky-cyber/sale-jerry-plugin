/**
 * 案例匹配功能
 *
 * 根据用户输入的企业名称和关注模块,从案例库中匹配相关案例
 * 匹配规则:相同行业、相同模块、优先一年内案例,不够3个则扩展到三年内
 */

// 案例接口定义
interface CaseRecord {
  customerName: string;      // 客户名称
  industry: string;          // 行业细分
  module: string;            // 模块
  contractName: string;      // 合同名称
  contractAmount: string;    // 合同金额
  contractDate: string;      // 合同时间
}

// 匹配参数接口
interface MatchParams {
  industry: string;          // 目标行业
  module: string;            // 目标模块
  currentDate?: Date;        // 当前日期,用于计算时间范围
  minCases?: number;         // 最少案例数量,默认3个
}

// 匹配结果接口
interface MatchResult {
  cases: CaseRecord[];       // 匹配的案例列表
  matchedCount: number;      // 匹配数量
  timeRange: string;         // 实际使用的时间范围
  matchCriteria: {
    industry: string;
    module: string;
  };
}

/**
 * 解析案例库markdown文件内容
 *
 * @param markdownContent - 案例库markdown内容
 * @returns 解析后的案例数组
 */
export function parseCaseLibrary(markdownContent: string): CaseRecord[] {
  const cases: CaseRecord[] = [];
  const lines = markdownContent.split('\n');

  // 跳过表头,从数据行开始解析
  let inDataSection = false;

  for (const line of lines) {
    // 检测是否到达表格数据区域
    if (line.includes('|---------|')) {
      inDataSection = true;
      continue;
    }

    // 如果遇到空行或统计信息区域,停止解析
    if (inDataSection && (!line.trim() || line.startsWith('##'))) {
      break;
    }

    // 解析数据行
    if (inDataSection && line.startsWith('|') && !line.includes('客户名称')) {
      const columns = line.split('|')
        .map(col => col.trim())
        .filter(col => col !== '');

      if (columns.length >= 6) {
        cases.push({
          customerName: columns[0],
          industry: columns[1],
          module: columns[2],
          contractName: columns[3],
          contractAmount: columns[4],
          contractDate: columns[5],
        });
      }
    }
  }

  return cases;
}

/**
 * 解析合同日期字符串
 *
 * @param dateStr - 日期字符串,如"2024年3月"
 * @returns Date对象
 */
function parseContractDate(dateStr: string): Date {
  const match = dateStr.match(/(\d{4})年(\d{1,2})月/);
  if (match) {
    const year = parseInt(match[1]);
    const month = parseInt(match[2]);
    return new Date(year, month - 1, 1);
  }
  return new Date(0); // 无法解析时返回最早日期
}

/**
 * 检查模块是否匹配
 *
 * @param caseModule - 案例的模块字符串
 * @param targetModule - 目标模块
 * @returns 是否匹配
 */
function isModuleMatch(caseModule: string, targetModule: string): boolean {
  // 将模块字符串按+或、分割
  const caseModules = caseModule.split(/[+、]/).map(m => m.trim());
  const targetModuleNormalized = targetModule.trim().toLowerCase();

  // 检查是否有任一模块匹配
  return caseModules.some(m => {
    const moduleNormalized = m.toLowerCase();
    return moduleNormalized.includes(targetModuleNormalized) ||
           targetModuleNormalized.includes(moduleNormalized);
  });
}

/**
 * 匹配案例
 *
 * @param cases - 所有案例
 * @param params - 匹配参数
 * @returns 匹配结果
 */
export function matchCases(
  cases: CaseRecord[],
  params: MatchParams
): MatchResult {
  const {
    industry,
    module,
    currentDate = new Date(),
    minCases = 3
  } = params;

  // 计算一年前和三年前的日期
  const oneYearAgo = new Date(currentDate);
  oneYearAgo.setFullYear(currentDate.getFullYear() - 1);

  const threeYearsAgo = new Date(currentDate);
  threeYearsAgo.setFullYear(currentDate.getFullYear() - 3);

  // 第一步:按行业和模块筛选
  const industryAndModuleMatched = cases.filter(c => {
    const industryMatch = c.industry === industry;
    const moduleMatch = isModuleMatch(c.module, module);
    return industryMatch && moduleMatch;
  });

  // 第二步:按时间筛选 - 优先一年内
  let matchedCases = industryAndModuleMatched.filter(c => {
    const caseDate = parseContractDate(c.contractDate);
    return caseDate >= oneYearAgo;
  });

  // 按日期降序排序(最新的在前)
  matchedCases.sort((a, b) => {
    const dateA = parseContractDate(a.contractDate);
    const dateB = parseContractDate(b.contractDate);
    return dateB.getTime() - dateA.getTime();
  });

  let timeRange = '一年内';

  // 如果一年内案例不够3个,扩展到三年内
  if (matchedCases.length < minCases) {
    matchedCases = industryAndModuleMatched.filter(c => {
      const caseDate = parseContractDate(c.contractDate);
      return caseDate >= threeYearsAgo;
    });

    // 重新按日期降序排序
    matchedCases.sort((a, b) => {
      const dateA = parseContractDate(a.contractDate);
      const dateB = parseContractDate(b.contractDate);
      return dateB.getTime() - dateA.getTime();
    });

    timeRange = '三年内';
  }

  return {
    cases: matchedCases,
    matchedCount: matchedCases.length,
    timeRange,
    matchCriteria: {
      industry,
      module,
    },
  };
}

/**
 * 格式化匹配结果为markdown表格
 *
 * @param result - 匹配结果
 * @returns markdown格式的字符串
 */
export function formatMatchResult(result: MatchResult): string {
  if (result.matchedCount === 0) {
    return `
### 匹配的案例

未找到符合条件的案例。

**匹配条件**:
- 行业: ${result.matchCriteria.industry}
- 模块: ${result.matchCriteria.module}
- 时间范围: 三年内

**建议**: 可以尝试扩大搜索范围或调整匹配条件。
`.trim();
  }

  const tableHeader = `
### 匹配的案例 (${result.timeRange})

**匹配条件**:
- 行业: ${result.matchCriteria.industry}
- 模块: ${result.matchCriteria.module}
- 匹配数量: ${result.matchedCount}个
- 时间范围: ${result.timeRange}

| 客户名称 | 模块 | 合同名称 | 合同金额 | 合同时间 |
|---------|------|---------|---------|---------|
`.trim();

  const tableRows = result.cases.map(c =>
    `| ${c.customerName} | ${c.module} | ${c.contractName} | ${c.contractAmount} | ${c.contractDate} |`
  ).join('\n');

  return `${tableHeader}\n${tableRows}`;
}

/**
 * 主函数:从markdown文件内容中匹配案例
 *
 * @param markdownContent - 案例库markdown内容
 * @param params - 匹配参数
 * @returns 格式化的匹配结果
 */
export function matchCasesFromMarkdown(
  markdownContent: string,
  params: MatchParams
): string {
  const cases = parseCaseLibrary(markdownContent);
  const result = matchCases(cases, params);
  return formatMatchResult(result);
}

// 导出默认函数
export default matchCasesFromMarkdown;
