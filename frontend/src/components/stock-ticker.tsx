import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { TrendingUp, TrendingDown } from "lucide-react";

const stockData = [
  { symbol: "삼성전자", price: "71,400", change: "+1,200", changePercent: "+1.71%", type: "positive" },
  { symbol: "SK하이닉스", price: "125,500", change: "-2,500", changePercent: "-1.96%", type: "negative" },
  { symbol: "NAVER", price: "195,000", change: "+3,500", changePercent: "+1.83%", type: "positive" },
  { symbol: "카카오", price: "52,800", change: "-800", changePercent: "-1.49%", type: "negative" },
  { symbol: "LG에너지솔루션", price: "420,000", change: "+15,000", changePercent: "+3.70%", type: "positive" },
];

export function StockTicker() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>주요 종목</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {stockData.map((stock, index) => (
            <div key={index} className="flex items-center justify-between py-2 border-b last:border-b-0">
              <div>
                <p className="font-medium">{stock.symbol}</p>
                <p className="text-lg font-semibold">{stock.price}원</p>
              </div>
              <div className="text-right">
                <div className={`flex items-center gap-1 ${
                  stock.type === "positive" ? "text-green-600" : "text-red-600"
                }`}>
                  {stock.type === "positive" ? (
                    <TrendingUp className="size-4" />
                  ) : (
                    <TrendingDown className="size-4" />
                  )}
                  <span className="text-sm">{stock.change}</span>
                </div>
                <p className={`text-sm ${
                  stock.type === "positive" ? "text-green-600" : "text-red-600"
                }`}>
                  {stock.changePercent}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}