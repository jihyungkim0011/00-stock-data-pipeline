import { useState } from "react";
import { CompanySelector } from "./components/company-selector";
import { DailyStockChart } from "./components/daily-stock-chart";
import { TargetPriceChart } from "./components/target-price-chart";
import { FinancialMetricsChart } from "./components/financial-metrics-chart";
import { CompanyNewsFeed } from "./components/company-news-feed";

export default function App() {
  const [selectedCompanies, setSelectedCompanies] = useState<string[]>(["samsung", "sk_hynix"]);

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto p-4 space-y-4">
        {/* Header */}
        <div className="border-b pb-3">
          <h1 className="text-3xl font-bold">금융 데이터 분석 대시보드</h1>
          <p className="text-muted-foreground mt-1">
            기업별 주식 데이터 비교 분석 및 뉴스 모니터링
          </p>
        </div>

        {/* Company Selection */}
        <CompanySelector
          selectedCompanies={selectedCompanies}
          onSelectionChange={setSelectedCompanies}
        />

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Daily Stock Chart */}
          <DailyStockChart selectedCompanies={selectedCompanies} />
          
          {/* Target Price Chart */}
          <TargetPriceChart selectedCompanies={selectedCompanies} />
        </div>

        {/* Financial Metrics Chart */}
        <FinancialMetricsChart
          selectedCompanies={selectedCompanies}
        />

        {/* Company News Feed */}
        <CompanyNewsFeed selectedCompanies={selectedCompanies} />
      </div>
    </div>
  );
}