import { Card, CardContent } from "./ui/card";
import { TrendingUp, TrendingDown } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string;
  change: string;
  changeType: "positive" | "negative";
  icon?: React.ReactNode;
}

export function MetricCard({ title, value, change, changeType, icon }: MetricCardProps) {
  const ChangeIcon = changeType === "positive" ? TrendingUp : TrendingDown;
  const changeColor = changeType === "positive" ? "text-green-600" : "text-red-600";
  const changeBgColor = changeType === "positive" ? "bg-green-50" : "bg-red-50";

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">{title}</p>
            <p className="text-2xl font-semibold mt-1">{value}</p>
            <div className={`flex items-center gap-1 mt-2 ${changeBgColor} px-2 py-1 rounded-full w-fit`}>
              <ChangeIcon className={`size-3 ${changeColor}`} />
              <span className={`text-xs ${changeColor}`}>{change}</span>
            </div>
          </div>
          {icon && (
            <div className="size-12 bg-primary/10 rounded-lg flex items-center justify-center">
              {icon}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}