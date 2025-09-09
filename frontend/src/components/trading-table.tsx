import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Badge } from "./ui/badge";

const tradingData = [
  {
    date: "2024-09-08",
    type: "매수",
    stock: "삼성전자",
    quantity: 100,
    price: "70,200",
    amount: "7,020,000",
    status: "체결"
  },
  {
    date: "2024-09-07",
    type: "매도",
    stock: "SK하이닉스",
    quantity: 50,
    price: "128,000",
    amount: "6,400,000",
    status: "체결"
  },
  {
    date: "2024-09-06",
    type: "매수",
    stock: "NAVER",
    quantity: 20,
    price: "191,500",
    amount: "3,830,000",
    status: "체결"
  },
  {
    date: "2024-09-05",
    type: "매수",
    stock: "카카오",
    quantity: 150,
    price: "53,600",
    amount: "8,040,000",
    status: "대기"
  },
  {
    date: "2024-09-04",
    type: "매도",
    stock: "LG에너지솔루션",
    quantity: 10,
    price: "405,000",
    amount: "4,050,000",
    status: "체결"
  },
];

export function TradingTable() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>최근 거래내역</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>날짜</TableHead>
              <TableHead>구분</TableHead>
              <TableHead>종목명</TableHead>
              <TableHead>수량</TableHead>
              <TableHead>단가</TableHead>
              <TableHead>총액</TableHead>
              <TableHead>상태</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tradingData.map((trade, index) => (
              <TableRow key={index}>
                <TableCell>{trade.date}</TableCell>
                <TableCell>
                  <Badge variant={trade.type === "매수" ? "default" : "secondary"}>
                    {trade.type}
                  </Badge>
                </TableCell>
                <TableCell>{trade.stock}</TableCell>
                <TableCell>{trade.quantity}주</TableCell>
                <TableCell>{trade.price}원</TableCell>
                <TableCell>{trade.amount}원</TableCell>
                <TableCell>
                  <Badge variant={trade.status === "체결" ? "default" : "outline"}>
                    {trade.status}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}