import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, CartesianGrid, ReferenceLine, Legend } from "recharts";
import { availableCompanies } from "./company-selector";

// 모의 적정주가 데이터
const getTargetPriceData = (companyId: string) => {
  const company = availableCompanies.find(c => c.id === companyId);
  if (!company) return null;

  // 기본 모의 데이터 (실제로는 API에서 가져와야 함)
  const basePrice = {
    samsung: 75000,
    sk_hynix: 125000,
    naver: 180000,
    kakao: 65000,
    lg_energy: 520000,
    hyundai_motor: 195000,
    posco: 290000,
    lg_chem: 480000,
    celltrion: 175000,
    kia: 95000,
    ncsoft: 220000,
    nexon: 24000,
    samsung_bio: 750000,
    hanwha_solutions: 32000,
  }[companyId] || 100000;

  const currentPrice = basePrice * 0.85; // 현재가는 적정가보다 15% 낮다고 가정

  return {
    company: company.name,
    currentPrice,
    data: [
      {
        scenario: "지속시",
        연간기준: Math.round(basePrice),
        분기기준: Math.round(basePrice * 0.95),
      },
      {
        scenario: "10% 감소시",
        연간기준: Math.round(basePrice * 0.9),
        분기기준: Math.round(basePrice * 0.85),
      },
      {
        scenario: "20% 감소시",
        연간기준: Math.round(basePrice * 0.8),
        분기기준: Math.round(basePrice * 0.75),
      },
      {
        scenario: "30% 감소시",
        연간기준: Math.round(basePrice * 0.7),
        분기기준: Math.round(basePrice * 0.65),
      },
    ],
  };
};

interface TargetPriceChartProps {
  selectedCompanies: string[];
}

export function TargetPriceChart({ selectedCompanies }: TargetPriceChartProps) {
  const primaryCompany = selectedCompanies[0];
  const targetData = primaryCompany ? getTargetPriceData(primaryCompany) : null;

  if (!targetData) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>적정주가 분석</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            기업을 선택해주세요
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>적정주가 분석</CardTitle>
        <p className="text-sm text-muted-foreground">
          {targetData.company} • 현재가: {targetData.currentPrice.toLocaleString()}원
        </p>
      </CardHeader>
      <CardContent>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={targetData.data}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="scenario" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={60}
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => `${(value / 1000).toFixed(0)}K`}
              />
              <Legend />
              
              {/* 현재가격 기준선 */}
              <ReferenceLine 
                y={targetData.currentPrice} 
                stroke="#ef4444" 
                strokeDasharray="5 5"
                label={{ value: "현재가", position: "left" }}
              />
              
              <Bar 
                dataKey="연간기준" 
                fill="var(--color-chart-1)" 
                name="연간기준 적정가"
                radius={[2, 2, 0, 0]}
              />
              <Bar 
                dataKey="분기기준" 
                fill="var(--color-chart-3)" 
                name="분기기준 적정가"
                radius={[2, 2, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="mt-4 text-xs text-muted-foreground">
          <p>• 빨간 점선: 현재 주가</p>
          <p>• 시나리오별 적정주가 범위를 보여줍니다</p>
        </div>
      </CardContent>
    </Card>
  );
}