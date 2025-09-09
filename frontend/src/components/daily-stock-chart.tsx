import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { availableCompanies } from "./company-selector";

// 모의 일별 주식 데이터 (최근 30일)
const generateDailyData = () => {
  const data = [];
  const baseDate = new Date();
  
  for (let i = 29; i >= 0; i--) {
    const date = new Date(baseDate);
    date.setDate(date.getDate() - i);
    
    const entry: any = {
      date: date.toISOString().split('T')[0],
      displayDate: `${date.getMonth() + 1}/${date.getDate()}`,
    };

    // 각 기업의 주가 데이터 생성 (임의의 데이터)
    entry.samsung = 70000 + Math.random() * 10000 - 5000;
    entry.sk_hynix = 120000 + Math.random() * 20000 - 10000;
    entry.naver = 190000 + Math.random() * 15000 - 7500;
    entry.kakao = 50000 + Math.random() * 8000 - 4000;
    entry.lg_energy = 400000 + Math.random() * 50000 - 25000;
    entry.hyundai_motor = 180000 + Math.random() * 15000 - 7500;
    entry.posco = 250000 + Math.random() * 30000 - 15000;
    entry.lg_chem = 350000 + Math.random() * 40000 - 20000;
    entry.celltrion = 160000 + Math.random() * 20000 - 10000;
    entry.kia = 85000 + Math.random() * 10000 - 5000;

    data.push(entry);
  }
  
  return data;
};

const dailyStockData = generateDailyData();

const colors = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4", "#84cc16", "#f97316", "#6366f1"];

interface DailyStockChartProps {
  selectedCompanies: string[];
}

export function DailyStockChart({ selectedCompanies }: DailyStockChartProps) {
  if (selectedCompanies.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>일별 주식 차트</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center h-64">
          <p className="text-muted-foreground">분석할 기업을 선택해주세요.</p>
        </CardContent>
      </Card>
    );
  }

  const formatTooltipValue = (value: number) => {
    return `${value.toLocaleString()}원`;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>일별 주식 차트 (최근 30일)</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={dailyStockData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="displayDate" 
              stroke="#64748b"
              fontSize={12}
            />
            <YAxis 
              stroke="#64748b"
              fontSize={12}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip 
              formatter={(value: number, name: string) => [formatTooltipValue(value), getCompanyName(name)]}
              labelStyle={{ color: "#1e40af" }}
              contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
            />
            <Legend />
            {selectedCompanies.map((companyId, index) => (
              <Line
                key={companyId}
                type="monotone"
                dataKey={companyId}
                stroke={colors[index % colors.length]}
                strokeWidth={2}
                name={getCompanyName(companyId)}
                dot={false}
                activeDot={{ r: 4, stroke: colors[index % colors.length], strokeWidth: 2 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

function getCompanyName(companyId: string): string {
  const company = availableCompanies.find(c => c.id === companyId);
  return company ? company.name : companyId;
}