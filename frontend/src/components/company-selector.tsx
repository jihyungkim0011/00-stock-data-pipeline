import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Checkbox } from "./ui/checkbox";
import { Badge } from "./ui/badge";
import { Input } from "./ui/input";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "./ui/collapsible";
import { X, Search, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "./ui/button";

const availableCompanies = [
  // 대기업 (시가총액 상위)
  { id: "samsung", name: "삼성전자", code: "005930", sector: "반도체", category: "대기업" },
  { id: "sk_hynix", name: "SK하이닉스", code: "000660", sector: "반도체", category: "대기업" },
  { id: "lg_energy", name: "LG에너지솔루션", code: "373220", sector: "배터리", category: "대기업" },
  { id: "hyundai_motor", name: "현대차", code: "005380", sector: "자동차", category: "대기업" },
  { id: "posco", name: "POSCO홀딩스", code: "005490", sector: "철강", category: "대기업" },
  
  // IT/테크
  { id: "naver", name: "NAVER", code: "035420", sector: "인터넷", category: "IT/테크" },
  { id: "kakao", name: "카카오", code: "035720", sector: "인터넷", category: "IT/테크" },
  { id: "ncsoft", name: "엔씨소프트", code: "036570", sector: "게임", category: "IT/테크" },
  { id: "nexon", name: "넥슨게임즈", code: "225570", sector: "게임", category: "IT/테크" },
  
  // 화학/바이오
  { id: "lg_chem", name: "LG화학", code: "051910", sector: "화학", category: "화학/바이오" },
  { id: "celltrion", name: "셀트리온", code: "068270", sector: "바이오", category: "화학/바이오" },
  { id: "samsung_bio", name: "삼성바이오로직스", code: "207940", sector: "바이오", category: "화학/바이오" },
  
  // 기타
  { id: "kia", name: "기아", code: "000270", sector: "자동차", category: "기타" },
  { id: "hanwha_solutions", name: "한화솔루션", code: "009830", sector: "화학", category: "기타" },
];

const sectors = ["전체", "반도체", "인터넷", "게임", "배터리", "자동차", "철강", "화학", "바이오"];

interface CompanySelectorProps {
  selectedCompanies: string[];
  onSelectionChange: (companies: string[]) => void;
}

export function CompanySelector({ selectedCompanies, onSelectionChange }: CompanySelectorProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSector, setSelectedSector] = useState("전체");
  const [isOpen, setIsOpen] = useState(false);

  const handleCompanyToggle = (companyId: string) => {
    const newSelection = selectedCompanies.includes(companyId)
      ? selectedCompanies.filter(id => id !== companyId)
      : [...selectedCompanies, companyId];
    onSelectionChange(newSelection);
  };

  const handleRemoveCompany = (companyId: string) => {
    onSelectionChange(selectedCompanies.filter(id => id !== companyId));
  };

  const getCompanyInfo = (id: string) => {
    return availableCompanies.find(company => company.id === id);
  };

  const filteredCompanies = availableCompanies.filter(company => {
    const matchesSearch = company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         company.code.includes(searchTerm);
    const matchesSector = selectedSector === "전체" || company.sector === selectedSector;
    return matchesSearch && matchesSector;
  });

  return (
    <div className="space-y-3">
      {/* Selected Companies */}
      {selectedCompanies.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-medium text-sm">선택된 기업 ({selectedCompanies.length}개)</h3>
          <div className="flex flex-wrap gap-2">
            {selectedCompanies.map(companyId => {
              const company = getCompanyInfo(companyId);
              return (
                <Badge key={companyId} variant="secondary" className="px-2 py-1 text-xs">
                  {company?.name}
                  <button
                    onClick={() => handleRemoveCompany(companyId)}
                    className="ml-1 hover:bg-destructive hover:text-destructive-foreground rounded-full p-0.5"
                  >
                    <X className="size-2" />
                  </button>
                </Badge>
              );
            })}
          </div>
        </div>
      )}

      {/* Company Selection - Collapsible */}
      <Collapsible open={isOpen} onOpenChange={setIsOpen}>
        <CollapsibleTrigger asChild>
          <Button variant="outline" className="w-full justify-between p-3 h-auto">
            <span className="text-sm font-medium">기업 선택</span>
            {isOpen ? <ChevronUp className="size-4" /> : <ChevronDown className="size-4" />}
          </Button>
        </CollapsibleTrigger>
        <CollapsibleContent>
          <Card className="mt-2">
            <CardContent className="p-4">
              {/* Search */}
              <div className="relative mb-4">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 size-4 text-muted-foreground" />
                <Input
                  placeholder="기업명, 종목코드로 검색..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 h-8"
                />
              </div>

              {/* Left-Right Split Layout */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Left: Sector Selection */}
                <div className="md:col-span-1">
                  <h4 className="font-medium text-sm mb-2">업종 선택</h4>
                  <div className="space-y-1 max-h-32 overflow-y-auto">
                    {sectors.map(sector => (
                      <button
                        key={sector}
                        onClick={() => setSelectedSector(sector)}
                        className={`w-full text-left px-2 py-1.5 rounded text-xs transition-colors ${
                          selectedSector === sector
                            ? "bg-primary text-primary-foreground"
                            : "hover:bg-muted"
                        }`}
                      >
                        {sector}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Right: Company Selection */}
                <div className="md:col-span-3">
                  <h4 className="font-medium text-sm mb-2">
                    기업 선택 {selectedSector !== "전체" && `(${selectedSector})`}
                  </h4>
                  <div className="grid grid-cols-2 lg:grid-cols-3 gap-1 max-h-32 overflow-y-auto">
                    {filteredCompanies.map(company => (
                      <div key={company.id} className="flex items-center space-x-2 p-1.5 rounded hover:bg-muted">
                        <Checkbox
                          id={company.id}
                          checked={selectedCompanies.includes(company.id)}
                          onCheckedChange={() => handleCompanyToggle(company.id)}
                        />
                        <div className="flex-1 min-w-0">
                          <label 
                            htmlFor={company.id}
                            className="cursor-pointer block"
                          >
                            <div className="font-medium truncate text-xs">{company.name}</div>
                            <div className="text-xs text-muted-foreground">
                              {company.code}
                            </div>
                          </label>
                        </div>
                      </div>
                    ))}
                    {filteredCompanies.length === 0 && (
                      <div className="col-span-full text-center py-4 text-muted-foreground text-xs">
                        검색 결과가 없습니다.
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </CollapsibleContent>
      </Collapsible>
    </div>
  );
}

export { availableCompanies };