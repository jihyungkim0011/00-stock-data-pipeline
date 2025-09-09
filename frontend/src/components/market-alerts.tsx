import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Alert, AlertDescription } from "./ui/alert";
import { Bell, TrendingUp, TrendingDown, AlertTriangle } from "lucide-react";

const alerts = [
  {
    type: "price",
    icon: TrendingUp,
    title: "가격 알림",
    message: "삼성전자가 목표가 72,000원에 도달했습니다.",
    time: "5분 전",
    severity: "success"
  },
  {
    type: "news",
    icon: Bell,
    title: "시장 뉴스",
    message: "한국은행 기준금리 동결 발표",
    time: "30분 전",
    severity: "info"
  },
  {
    type: "warning",
    icon: AlertTriangle,
    title: "리스크 알림",
    message: "포트폴리오 집중도가 높습니다. 분산투자를 고려해보세요.",
    time: "1시간 전",
    severity: "warning"
  },
  {
    type: "loss",
    icon: TrendingDown,
    title: "손실 알림",
    message: "SK하이닉스가 설정한 손절가에 근접했습니다.",
    time: "2시간 전",
    severity: "error"
  }
];

export function MarketAlerts() {
  const getSeverityClass = (severity: string) => {
    switch (severity) {
      case "success": return "border-green-200 bg-green-50";
      case "warning": return "border-yellow-200 bg-yellow-50";
      case "error": return "border-red-200 bg-red-50";
      default: return "border-blue-200 bg-blue-50";
    }
  };

  const getIconColor = (severity: string) => {
    switch (severity) {
      case "success": return "text-green-600";
      case "warning": return "text-yellow-600";
      case "error": return "text-red-600";
      default: return "text-blue-600";
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>시장 알림</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {alerts.map((alert, index) => (
            <Alert key={index} className={getSeverityClass(alert.severity)}>
              <alert.icon className={`size-4 ${getIconColor(alert.severity)}`} />
              <AlertDescription>
                <div className="space-y-1">
                  <div className="flex justify-between items-start">
                    <span className="font-medium text-sm">{alert.title}</span>
                    <span className="text-xs text-muted-foreground">{alert.time}</span>
                  </div>
                  <p className="text-sm">{alert.message}</p>
                </div>
              </AlertDescription>
            </Alert>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}