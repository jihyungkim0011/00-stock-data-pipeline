import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const portfolioData = [
  { month: "1월", value: 100000000, benchmark: 100000000 },
  { month: "2월", value: 105000000, benchmark: 102000000 },
  { month: "3월", value: 98000000, benchmark: 99000000 },
  { month: "4월", value: 112000000, benchmark: 105000000 },
  { month: "5월", value: 120000000, benchmark: 108000000 },
  { month: "6월", value: 115000000, benchmark: 106000000 },
  { month: "7월", value: 125000000, benchmark: 110000000 },
  { month: "8월", value: 130000000, benchmark: 112000000 },
  { month: "9월", value: 135000000, benchmark: 115000000 },
];

export function PortfolioChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>포트폴리오 성과</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={portfolioData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="month" 
              stroke="#64748b"
              fontSize={12}
            />
            <YAxis 
              stroke="#64748b"
              fontSize={12}
              tickFormatter={(value) => `${(value / 100000000).toFixed(1)}억`}
            />
            <Tooltip 
              formatter={(value: number) => [`${(value / 100000000).toFixed(1)}억원`, ""]}
              labelStyle={{ color: "#1e40af" }}
              contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
            />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke="hsl(var(--chart-1))" 
              strokeWidth={3}
              name="내 포트폴리오"
              dot={{ fill: "hsl(var(--chart-1))", strokeWidth: 2, r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="benchmark" 
              stroke="hsl(var(--chart-2))" 
              strokeWidth={2}
              strokeDasharray="5 5"
              name="벤치마크"
              dot={{ fill: "hsl(var(--chart-2))", strokeWidth: 2, r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}