import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { availableCompanies } from "./company-selector";

// 모의 재무지표 데이터
const financialMetricsData: Record<string, any> = {
  samsung: {
    name: "삼성전자",
    EPS: 5420,
    ROE: 9.8,
    ROA: 6.2,
    BPS: 55280,
    "EV/EBITDA": 8.5,
    PER: 13.2,
    PBR: 1.3,
    "부채비율": 45.2
  },
  sk_hynix: {
    name: "SK하이닉스",
    EPS: 8950,
    ROE: 15.2,
    ROA: 8.9,
    BPS: 58900,
    "EV/EBITDA": 6.8,
    PER: 14.1,
    PBR: 2.1,
    "부채비율": 38.7
  },
  naver: {
    name: "NAVER",
    EPS: 12500,
    ROE: 11.5,
    ROA: 7.8,
    BPS: 108750,
    "EV/EBITDA": 12.3,
    PER: 15.6,
    PBR: 1.8,
    "부채비율": 22.1
  },
  kakao: {
    name: "카카오",
    EPS: 3200,
    ROE: 6.8,
    ROA: 4.2,
    BPS: 47050,
    "EV/EBITDA": 18.9,
    PER: 16.5,
    PBR: 1.1,
    "부채비율": 31.5
  },
  lg_energy: {
    name: "LG에너지솔루션",
    EPS: 15600,
    ROE: 18.5,
    ROA: 12.3,
    BPS: 84300,
    "EV/EBITDA": 9.2,
    PER: 27.0,
    PBR: 5.0,
    "부채비율": 58.9
  },
  hyundai_motor: {
    name: "현대차",
    EPS: 18900,
    ROE: 8.9,
    ROA: 3.8,
    BPS: 212400,
    "EV/EBITDA": 5.6,
    PER: 9.5,
    PBR: 0.8,
    "부채비율": 72.3
  },
  posco: {
    name: "POSCO홀딩스",
    EPS: 22100,
    ROE: 12.4,
    ROA: 6.8,
    BPS: 178200,
    "EV/EBITDA": 4.2,
    PER: 11.3,
    PBR: 1.4,
    "부채비율": 42.8
  },
  lg_chem: {
    name: "LG화학",
    EPS: 16800,
    ROE: 7.2,
    ROA: 4.1,
    BPS: 233100,
    "EV/EBITDA": 7.8,
    PER: 20.8,
    PBR: 1.5,
    "부채비율": 49.7
  },
  celltrion: {
    name: "셀트리온",
    EPS: 8950,
    ROE: 14.6,
    ROA: 9.8,
    BPS: 61300,
    "EV/EBITDA": 11.5,
    PER: 17.9,
    PBR: 2.6,
    "부채비율": 28.4
  },
  kia: {
    name: "기아",
    EPS: 12400,
    ROE: 11.8,
    ROA: 4.9,
    BPS: 105100,
    "EV/EBITDA": 3.8,
    PER: 6.9,
    PBR: 0.8,
    "부채비율": 65.1
  }
};

interface FinancialMetricsChartProps {
  selectedCompanies: string[];
}

const metrics = [
  { key: "EPS", label: "EPS", unit: "원", format: (val: number) => `${val.toLocaleString()}원` },
  { key: "ROE", label: "ROE", unit: "%", format: (val: number) => `${val}%` },
  { key: "ROA", label: "ROA", unit: "%", format: (val: number) => `${val}%` },
  { key: "BPS", label: "BPS", unit: "원", format: (val: number) => `${val.toLocaleString()}원` },
  { key: "EV/EBITDA", label: "EV/EBITDA", unit: "배", format: (val: number) => `${val}배` },
  { key: "PER", label: "PER", unit: "배", format: (val: number) => `${val}배` },
  { key: "PBR", label: "PBR", unit: "배", format: (val: number) => `${val}배` },
  { key: "부채비율", label: "부채비율", unit: "%", format: (val: number) => `${val}%` }
];

// 기업별 색상 매핑
const companyColors = [
  "#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", 
  "#ec4899", "#06b6d4", "#84cc16", "#f97316", "#6366f1"
];

export function FinancialMetricsChart({ selectedCompanies }: FinancialMetricsChartProps) {
  if (selectedCompanies.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>재무지표 비교</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center h-64">
          <p className="text-muted-foreground">분석할 기업을 선택해주세요.</p>
        </CardContent>
      </Card>
    );
  }

  // 각 지표별로 차트 데이터 생성
  const generateChartData = (metricKey: string) => {
    return selectedCompanies.map((companyId, index) => ({
      company: financialMetricsData[companyId]?.name || companyId,
      value: financialMetricsData[companyId]?.[metricKey] || 0,
      fill: companyColors[index % companyColors.length],
      companyId,
      companyIndex: index
    }));
  };

  const formatYAxisTick = (value: number, metricKey: string) => {
    if (metricKey === "EPS" || metricKey === "BPS") {
      return `${(value / 1000).toFixed(0)}k`;
    }
    return value.toString();
  };

  const CustomTooltip = ({ active, payload, label, metricInfo }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium">{label}</p>
          <p className="text-primary">
            {metricInfo.label}: {metricInfo.format(payload[0].value)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>재무지표 비교 분석</CardTitle>
        <p className="text-sm text-muted-foreground">
          선택된 기업들의 주요 재무지표를 비교합니다
        </p>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {metrics.map((metric, index) => {
            const chartData = generateChartData(metric.key);
            
            return (
              <div key={metric.key} className="border rounded-lg p-3 bg-card min-h-[280px]">
                <h4 className="font-medium text-center mb-3 text-sm">{metric.label}</h4>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart 
                    data={chartData} 
                    margin={{ top: 10, right: 10, left: 10, bottom: 25 }}
                    maxBarSize={Math.max(40, 200 / selectedCompanies.length)}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis 
                      dataKey="company" 
                      stroke="#64748b"
                      fontSize={10}
                      angle={selectedCompanies.length > 3 ? -45 : 0}
                      textAnchor={selectedCompanies.length > 3 ? "end" : "middle"}
                      height={selectedCompanies.length > 3 ? 60 : 40}
                      interval={0}
                      tick={{ fontSize: 10 }}
                    />
                    <YAxis 
                      stroke="#64748b"
                      fontSize={10}
                      tickFormatter={(value) => formatYAxisTick(value, metric.key)}
                      width={40}
                    />
                    <Tooltip 
                      content={(props) => (
                        <CustomTooltip {...props} metricInfo={metric} />
                      )}
                    />
                    <Bar 
                      dataKey="value" 
                      radius={[3, 3, 0, 0]}
                    >
                      {chartData.map((entry, idx) => (
                        <Cell key={`cell-${idx}`} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            );
          })}
        </div>
        
        {/* 범례 */}
        <div className="mt-6 pt-4 border-t">
          <h5 className="font-medium mb-3">선택된 기업</h5>
          <div className="flex flex-wrap gap-4">
            {selectedCompanies.map((companyId, index) => {
              const companyName = financialMetricsData[companyId]?.name || companyId;
              const color = companyColors[index % companyColors.length];
              
              return (
                <div key={companyId} className="flex items-center gap-2">
                  <div 
                    className="w-4 h-4 rounded-sm flex-shrink-0" 
                    style={{ backgroundColor: color }}
                  />
                  <span className="text-sm font-medium">{companyName}</span>
                </div>
              );
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}