import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

const allocationData = [
  { name: "국내주식", value: 45, color: "hsl(var(--chart-1))" },
  { name: "해외주식", value: 30, color: "hsl(var(--chart-2))" },
  { name: "채권", value: 15, color: "hsl(var(--chart-3))" },
  { name: "현금", value: 7, color: "hsl(var(--chart-4))" },
  { name: "기타", value: 3, color: "hsl(var(--chart-5))" },
];

export function AssetAllocationChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>자산 배분</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={allocationData}
              cx="50%"
              cy="50%"
              outerRadius={80}
              dataKey="value"
              label={({ name, value }) => `${name} ${value}%`}
              labelLine={false}
            >
              {allocationData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              formatter={(value) => [`${value}%`, ""]} 
              contentStyle={{ backgroundColor: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px" }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="grid grid-cols-2 gap-2 mt-4">
          {allocationData.map((item, index) => (
            <div key={index} className="flex items-center gap-2">
              <div 
                className="size-3 rounded-full" 
                style={{ backgroundColor: item.color }}
              />
              <span className="text-sm">{item.name}: {item.value}%</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}