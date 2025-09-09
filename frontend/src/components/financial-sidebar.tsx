import { BarChart3, Home, PieChart, TrendingUp, Wallet, Bell, Settings, User } from "lucide-react";
import { Sidebar, SidebarContent, SidebarHeader, SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarFooter } from "./ui/sidebar";

const menuItems = [
  { icon: Home, label: "대시보드", id: "dashboard" },
  { icon: Wallet, label: "포트폴리오", id: "portfolio" },
  { icon: TrendingUp, label: "주식", id: "stocks" },
  { icon: BarChart3, label: "분석", id: "analytics" },
  { icon: PieChart, label: "리포트", id: "reports" },
  { icon: Bell, label: "알림", id: "alerts" },
];

interface FinancialSidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

export function FinancialSidebar({ activeSection, onSectionChange }: FinancialSidebarProps) {
  return (
    <Sidebar className="border-r">
      <SidebarHeader className="p-6">
        <div className="flex items-center gap-2">
          <div className="size-8 bg-primary rounded-lg flex items-center justify-center">
            <TrendingUp className="size-4 text-primary-foreground" />
          </div>
          <h1 className="font-semibold">FinanceHub</h1>
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarMenu>
          {menuItems.map((item) => (
            <SidebarMenuItem key={item.id}>
              <SidebarMenuButton 
                onClick={() => onSectionChange(item.id)}
                isActive={activeSection === item.id}
                className="w-full"
              >
                <item.icon className="size-4" />
                <span>{item.label}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>

      <SidebarFooter className="p-4">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton>
              <User className="size-4" />
              <span>프로필</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton>
              <Settings className="size-4" />
              <span>설정</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}