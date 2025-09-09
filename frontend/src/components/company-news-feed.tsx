import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { ExternalLink, Clock } from "lucide-react";
import { availableCompanies } from "./company-selector";

// 모의 뉴스 데이터
const mockNewsData: Record<string, any[]> = {
  samsung: [
    {
      title: "삼성전자, 3분기 반도체 업황 회복세로 매출 증가 전망",
      summary: "메모리 반도체 가격 상승과 수요 회복으로 3분기 실적 개선 기대",
      time: "2시간 전",
      source: "한국경제",
      category: "실적"
    },
    {
      title: "삼성전자, AI 반도체 경쟁력 강화를 위한 대규모 투자 발표",
      summary: "차세대 AI 칩 개발에 10조원 규모 투자 계획 공개",
      time: "5시간 전",
      source: "전자신문",
      category: "투자"
    },
    {
      title: "삼성 갤럭시 S24, 글로벌 시장에서 호조세 지속",
      summary: "프리미엄 스마트폰 시장 점유율 확대로 모바일 부문 실적 향상",
      time: "8시간 전",
      source: "디지털타임스",
      category: "제품"
    }
  ],
  sk_hynix: [
    {
      title: "SK하이닉스, HBM3E 양산 본격화로 AI 메모리 시장 선점",
      summary: "고대역폭 메모리 HBM3E 양산 라인 가동으로 AI 반도체 공급망 강화",
      time: "1시간 전",
      source: "매일경제",
      category: "기술"
    },
    {
      title: "SK하이닉스 3분기 실적 전망, 메모리 업황 회복으로 흑자 전환 기대",
      summary: "DRAM과 NAND 플래시 가격 상승으로 분기 흑자 달성 전망",
      time: "4시간 전",
      source: "서울경제",
      category: "실적"
    }
  ],
  naver: [
    {
      title: "네이버, 생성형 AI '하이퍼클로바X' 기업 서비스 확대",
      summary: "B2B 시장 진출 가속화로 AI 사업 매출 성장 기대",
      time: "3시간 전",
      source: "IT조선",
      category: "서비스"
    },
    {
      title: "네이버페이, 간편결제 시장 점유율 2위 달성",
      summary: "핀테크 사업 확장으로 플랫폼 경쟁력 강화",
      time: "6시간 전",
      source: "파이낸셜뉴스",
      category: "사업"
    }
  ],
  kakao: [
    {
      title: "카카오, 택시·대리 통합 플랫폼 출시로 모빌리티 사업 강화",
      summary: "통합 모빌리티 서비스로 이용자 편의성 향상 및 시장 확대",
      time: "2시간 전",
      source: "아시아경제",
      category: "서비스"
    },
    {
      title: "카카오뱅크, 대출 포트폴리오 다각화로 수익성 개선",
      summary: "개인신용대출 외 주택담보대출 등으로 사업 영역 확장",
      time: "7시간 전",
      source: "연합뉴스",
      category: "금융"
    }
  ],
  lg_energy: [
    {
      title: "LG에너지솔루션, 북미 배터리 공장 증설로 생산 능력 확대",
      summary: "테슬라·GM 등 주요 고객사 대응을 위한 대규모 투자",
      time: "1시간 전",
      source: "조선비즈",
      category: "투자"
    }
  ],
  hyundai_motor: [
    {
      title: "현대차, 전기차 아이오닉 시리즈 글로벌 판매 호조",
      summary: "유럽·북미 시장에서 전기차 판매량 전년 대비 50% 증가",
      time: "4시간 전",
      source: "오토헤럴드",
      category: "판매"
    }
  ]
};

interface CompanyNewsFeedProps {
  selectedCompanies: string[];
}

export function CompanyNewsFeed({ selectedCompanies }: CompanyNewsFeedProps) {
  if (selectedCompanies.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>기업 뉴스</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center h-64">
          <p className="text-muted-foreground">뉴스를 확인할 기업을 선택해주세요.</p>
        </CardContent>
      </Card>
    );
  }

  // 선택된 기업들의 뉴스를 모두 수집하고 시간순으로 정렬
  const allNews = selectedCompanies
    .flatMap(companyId => {
      const companyNews = mockNewsData[companyId] || [];
      return companyNews.map(news => ({
        ...news,
        companyId,
        companyName: availableCompanies.find(c => c.id === companyId)?.name || companyId
      }));
    })
    .sort((a, b) => {
      // 간단한 시간 정렬 (실제로는 타임스탬프를 사용해야 함)
      const timeA = parseInt(a.time);
      const timeB = parseInt(b.time);
      return timeA - timeB;
    });

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      "실적": "bg-blue-100 text-blue-800",
      "투자": "bg-green-100 text-green-800",
      "제품": "bg-purple-100 text-purple-800",
      "기술": "bg-orange-100 text-orange-800",
      "서비스": "bg-cyan-100 text-cyan-800",
      "사업": "bg-gray-100 text-gray-800",
      "금융": "bg-yellow-100 text-yellow-800",
      "판매": "bg-pink-100 text-pink-800"
    };
    return colors[category] || "bg-gray-100 text-gray-800";
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>기업 뉴스 ({allNews.length}건)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {allNews.map((news, index) => (
            <div key={index} className="border-b pb-4 last:border-b-0">
              <div className="flex justify-between items-start gap-2 mb-2">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="text-xs">
                    {news.companyName}
                  </Badge>
                  <Badge className={`text-xs ${getCategoryColor(news.category)}`}>
                    {news.category}
                  </Badge>
                </div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground whitespace-nowrap">
                  <Clock className="size-3" />
                  {news.time}
                </div>
              </div>
              
              <h4 className="font-medium text-sm mb-1 line-clamp-2">{news.title}</h4>
              <p className="text-sm text-muted-foreground mb-2 line-clamp-2">{news.summary}</p>
              
              <div className="flex justify-between items-center">
                <span className="text-xs text-muted-foreground">{news.source}</span>
                <button className="flex items-center gap-1 text-xs text-primary hover:underline">
                  자세히 보기 <ExternalLink className="size-3" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}