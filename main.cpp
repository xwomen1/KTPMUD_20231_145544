#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <queue>
#include <cmath>
#include <algorithm>
#include <limits>
#include <memory>
#include <sstream>
#include <fstream>
#include <iomanip>
#include <ctime>
#include "httplib.h"
#include "json.hpp"
#include <sys/stat.h>
#ifdef _WIN32
#include <direct.h>
#endif

// Define M_PI if not defined
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

using json = nlohmann::json;
struct Student {
    std::string id;
    std::string name;
    std::string faculty;
    std::string licensePlate;
    double balance;
    std::vector<std::string> transactions;
    
    Student() : id(""), name(""), faculty(""), licensePlate(""), balance(0.0) {}
    Student(const std::string& id, const std::string& name, 
            const std::string& faculty, const std::string& licensePlate)
        : id(id), name(name), faculty(faculty), 
          licensePlate(licensePlate), balance(0.0) {}
};

// Chuyển đổi Student sang JSON
void to_json(json& j, const Student& s) {
    j = json{
        {"id", s.id},
        {"name", s.name},
        {"faculty", s.faculty},
        {"licensePlate", s.licensePlate},
        {"balance", s.balance},
        {"transactions", s.transactions}
    };
}

// Chuyển đổi JSON sang Student
void from_json(const json& j, Student& s) {
    j.at("id").get_to(s.id);
    j.at("name").get_to(s.name);
    j.at("faculty").get_to(s.faculty);
    j.at("licensePlate").get_to(s.licensePlate);
    if (j.contains("balance")) j.at("balance").get_to(s.balance);
    if (j.contains("transactions")) j.at("transactions").get_to(s.transactions);
}

const std::string STUDENT_DB_FILE = "students.json";

// Đọc danh sách sinh viên từ file
std::unordered_map<std::string, Student> LoadStudents() {
    std::unordered_map<std::string, Student> students;
    std::ifstream inFile(STUDENT_DB_FILE);
    
    if (inFile.good()) {
        json j;
        try {
            inFile >> j;
            for (const auto& item : j) {
                Student s = item.get<Student>();
                students[s.id] = s;
            }
        } catch (const std::exception& e) {
            std::cerr << "Error loading students: " << e.what() << std::endl;
        }
    }
    
    return students;
}

// Lưu danh sách sinh viên vào file
void SaveStudents(const std::unordered_map<std::string, Student>& students) {
    json j;
    for (const auto& pair : students) {
        j.push_back(pair.second);
    }
    
    std::ofstream outFile(STUDENT_DB_FILE);
    outFile << j.dump(4);
}

// Cấu trúc dữ liệu cho bãi xe
struct ParkingLot {
    std::string name;
    double lat;
    double lng;
    int capacity;
    int occupied;
    
    ParkingLot() : name(""), lat(0.0), lng(0.0), capacity(0), occupied(0) {}
    ParkingLot(const std::string& name, double lat, double lng, int capacity, int occupied)
        : name(name), lat(lat), lng(lng), capacity(capacity), occupied(occupied) {}
};

// Chuyển đổi ParkingLot sang JSON
void to_json(json& j, const ParkingLot& p) {
    j = json{
        {"name", p.name},
        {"lat", p.lat},
        {"lng", p.lng},
        {"capacity", p.capacity},
        {"occupied", p.occupied}
    };
}

// Chuyển đổi JSON sang ParkingLot
void from_json(const json& j, ParkingLot& p) {
    j.at("name").get_to(p.name);
    j.at("lat").get_to(p.lat);
    j.at("lng").get_to(p.lng);
    j.at("capacity").get_to(p.capacity);
    j.at("occupied").get_to(p.occupied);
}

const std::string PARKING_LOTS_FILE = "parking_lots.json";

// Đọc danh sách bãi xe từ file
std::unordered_map<std::string, ParkingLot> LoadParkingLots() {
    std::unordered_map<std::string, ParkingLot> parkingLots;
    std::ifstream inFile(PARKING_LOTS_FILE);
    
    if (inFile.good()) {
        try {
            json j;
            inFile >> j;
            for (const auto& item : j) {
                ParkingLot p = item.get<ParkingLot>();
                parkingLots[p.name] = p;
            }
        } catch (const std::exception& e) {
            std::cerr << "Error loading parking lots: " << e.what() << std::endl;
        }
    } else {
        // Tạo file mẫu nếu không tồn tại
        std::ofstream outFile(PARKING_LOTS_FILE);
        json j = json::array();
        outFile << j.dump(4);
    }
    
    return parkingLots;
}

// Lưu danh sách bãi xe vào file
void SaveParkingLots(const std::unordered_map<std::string, ParkingLot>& parkingLots) {
    json j;
    for (const auto& pair : parkingLots) {
        j.push_back(pair.second);
    }
    
    std::ofstream outFile(PARKING_LOTS_FILE);
    outFile << j.dump(4);
}

// Cấu trúc dữ liệu cho lịch sử đỗ xe
struct ParkingRecord {
    std::string parkingLot;
    std::string studentId;
    std::string licensePlate;
    std::string entryTime;
    std::string exitTime;
    double fee;
};

// Chuyển đổi ParkingRecord sang JSON
inline void to_json(json& j, const ParkingRecord& r) {
    j = json{
        {"parkingLot", r.parkingLot},
        {"studentId", r.studentId},
        {"licensePlate", r.licensePlate},
        {"entryTime", r.entryTime},
        {"exitTime", r.exitTime},
        {"fee", r.fee}
    };
}

// Chuyển đổi JSON sang ParkingRecord
inline void from_json(const json& j, ParkingRecord& r) {
    j.at("parkingLot").get_to(r.parkingLot);
    j.at("studentId").get_to(r.studentId);
    j.at("licensePlate").get_to(r.licensePlate);
    j.at("entryTime").get_to(r.entryTime);
    j.at("exitTime").get_to(r.exitTime);
    j.at("fee").get_to(r.fee);
}

const std::string PARKING_HISTORY_FILE = "parking_history.json";

// Đọc lịch sử đỗ xe từ file
std::vector<ParkingRecord> LoadParkingHistory() {
    std::vector<ParkingRecord> history;
    std::ifstream inFile(PARKING_HISTORY_FILE);
    
    if (inFile.good()) {
        try {
            json j;
            inFile >> j;
            for (const auto& item : j) {
                ParkingRecord r = item.get<ParkingRecord>();
                history.push_back(r);
            }
        } catch (const std::exception& e) {
            std::cerr << "Error loading parking history: " << e.what() << std::endl;
        }
    } else {
        // Tạo file mẫu nếu không tồn tại
        std::ofstream outFile(PARKING_HISTORY_FILE);
        json j = json::array();
        outFile << j.dump(4);
    }
    
    return history;
}

// Lưu lịch sử đỗ xe vào file
void SaveParkingHistory(const std::vector<ParkingRecord>& history) {
    json j;
    for (const auto& record : history) {
        j.push_back(record);
    }
    
    std::ofstream outFile(PARKING_HISTORY_FILE);
    outFile << j.dump(4);
}

// Hàm tạo timestamp hiện tại
std::string currentDateTime() {
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    
    std::stringstream ss;
    ss << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S");
    return ss.str();
}

// Hàm chuyển đổi chuỗi thời gian sang time_t
time_t stringToTime(const std::string& timeStr) {
    std::tm tm = {};
    std::istringstream ss(timeStr);
    ss >> std::get_time(&tm, "%Y-%m-%d %H:%M:%S");
    return std::mktime(&tm);
}

// Cấu trúc dữ liệu cho điểm
struct Point {
    std::string Name;
    double Lat;
    double Lng;
    int Capacity; // sức chứa tối đa
    int Occupied; // số xe hiện tại
    
    Point() : Name(""), Lat(0.0), Lng(0.0), Capacity(0), Occupied(0) {}
    Point(const std::string& name, double lat, double lng, int capacity, int occupied)
        : Name(name), Lat(lat), Lng(lng), Capacity(capacity), Occupied(occupied) {}
};

struct Coordinate {
    double lat;
    double lng;
    
    Coordinate() : lat(0.0), lng(0.0) {}
    Coordinate(double lat, double lng) : lat(lat), lng(lng) {}
};

// Convert Coordinate to JSON
void to_json(json& j, const Coordinate& c) {
    j = json{{"lat", c.lat}, {"lng", c.lng}};
}

// Convert JSON to Coordinate
void from_json(const json& j, Coordinate& c) {
    j.at("lat").get_to(c.lat);
    j.at("lng").get_to(c.lng);
}

// (Đã định nghĩa ở trên, xóa bản trùng lặp này)

// Database giả lập
std::unordered_map<std::string, Point> points = {
    {"Nha xe D9", Point("Nha xe D9", 21.004061, 105.844573, 300, 150)},
    {"Nha xe D3-5", Point("Nha xe D3-5", 21.004972, 105.845431, 500, 300)},
    {"Nha xe C7", Point("Nha xe C7", 21.005054, 105.844911, 300, 120)},
    {"Nha xe C5", Point("Nha xe C5", 21.005863, 105.844629, 200, 80)},
    {"Nha xe D4-6", Point("Nha xe D4-6", 21.004592, 105.842322, 300, 300)},
    {"Nha xe B1", Point("Nha xe B1", 21.005002, 105.846058, 100, 90)},
    {"Nha xe TC", Point("Nha xe TC", 21.002553, 105.847055, 500, 350)},
    {"Nha xe B13", Point("Nha xe B13", 21.006460, 105.847312, 100, 40)},
    {"Nha xe B6", Point("Nha xe B6", 21.006319, 105.846545, 100, 60)},

    // Các ngã rẽ
    {"Intersection D4-D6", Point("Intersection D4-D6", 21.005079, 105.842333, 0, 0)},
    {"Intersection TDN", Point("Intersection TDN", 21.005032, 105.845634, 0, 0)},
    {"Intersection D9-C5", Point("Intersection D9-C5", 21.005027, 105.844605, 0, 0)},
    {"Intersection B6", Point("Intersection B6", 21.005022, 105.846508, 0, 0)},
    {"Intersection B13TC", Point("Intersection B13TC", 21.004927, 105.846958, 0, 0)},
    {"Intersection TQB-TC", Point("Intersection TQB-TC", 21.003244, 105.847993, 0, 0)},
    {"Intersection TQB1", Point("Intersection TQB1", 21.004501, 105.847210, 0, 0)},
    {"Intersection TQB2", Point("Intersection TQB2", 21.004081, 105.847231, 0, 0)},
    {"Intersection quaydauTC", Point("Intersection quaydauTC", 21.001862, 105.846331, 0, 0)}
};

struct Edge {
    std::string To;
    int Weight;
    
    Edge(const std::string& to, int weight) : To(to), Weight(weight) {}
};

using Graph = std::unordered_map<std::string, std::vector<Edge>>;

Graph graph = {
    // Trục chính
    {"Intersection D4-D6", {Edge("Nha xe D4-6", 2), Edge("Intersection D9-C5", 10)}},
    {"Intersection TDN", {Edge("Nha xe C7", 3), Edge("Nha xe B1", 2)}},
    {"Intersection D9-C5", {Edge("Intersection D4-D6", 10), Edge("Nha xe D9", 4), Edge("Nha xe C5", 4), Edge("Nha xe C7", 1), Edge("Nha xe D3-5", 4)}},
    {"Intersection B6", {Edge("Nha xe B1", 1), Edge("Nha xe B6", 5), Edge("Intersection B13TC", 1)}},
    {"Intersection B13TC", {Edge("Intersection B6", 1), Edge("Intersection TQB1", 1), Edge("Nha xe B13", 6)}},
    {"Intersection TQB-TC", {Edge("Intersection TQB2", 3), Edge("Nha xe TC", 4)}},
    {"Intersection TQB1", {Edge("Intersection B13TC", 6), Edge("Intersection TQB2", 2)}},
    {"Intersection TQB2", {Edge("Intersection TQB1", 2), Edge("Intersection TQB-TC", 2)}},
    {"Intersection quaydauTC", {Edge("Intersection TQB-TC", 1)}},

    // Các nhà xe
    {"Nha xe C7", {Edge("Intersection D9-C5", 1)}},
    {"Nha xe C5", {Edge("Intersection D9-C5", 3)}},
    {"Nha xe D3-5", {Edge("Intersection TDN", 1)}},
    {"Nha xe D9", {Edge("Intersection D9-C5", 3)}},
    {"Nha xe D4-6", {Edge("Intersection D4-D6", 1)}},
    {"Nha xe B1", {Edge("Intersection TDN", 1), Edge("Intersection B6", 1)}},
    {"Nha xe B6", {Edge("Intersection B6", 5)}},
    {"Nha xe TC", {Edge("Intersection quaydauTC", 2)}},
    {"Nha xe B13", {Edge("Intersection B13TC", 6)}}
};

// Dijkstra
struct Item {
    std::string Node;
    int Distance;
    int Index;
    
    Item(const std::string& node, int distance) : Node(node), Distance(distance), Index(0) {}
};

struct ItemComparator {
    bool operator()(const Item& a, const Item& b) const {
        return a.Distance > b.Distance; // Min-heap (reverse comparison)
    }
};

std::pair<std::vector<std::string>, int> Dijkstra(const Graph& graph, const std::string& start, const std::string& end) {
    std::unordered_map<std::string, int> dist;
    std::unordered_map<std::string, std::string> prev;
    std::priority_queue<Item, std::vector<Item>, ItemComparator> pq;

    // Initialize distances
    for (const auto& node : graph) {
        dist[node.first] = std::numeric_limits<int>::max();
    }
    dist[start] = 0;
    pq.push(Item(start, 0));

    while (!pq.empty()) {
        Item u = pq.top();
        pq.pop();
        
        if (u.Node == end) {
            break;
        }
        
        auto it = graph.find(u.Node);
        if (it != graph.end()) {
            for (const Edge& edge : it->second) {
                int alt = dist[u.Node] + edge.Weight;
                if (alt < dist[edge.To]) {
                    dist[edge.To] = alt;
                    prev[edge.To] = u.Node;
                    pq.push(Item(edge.To, alt));
                }
            }
        }
    }

    std::vector<std::string> path;
    if (dist.find(end) == dist.end() || dist[end] == std::numeric_limits<int>::max()) {
        return std::make_pair(path, -1); // No path found
    }

    std::string u = end;
    while (!u.empty()) {
        path.insert(path.begin(), u);
        if (u == start) {
            break;
        }
        auto it = prev.find(u);
        if (it != prev.end()) {
            u = it->second;
        } else {
            break;
        }
    }
    
    return std::make_pair(path, dist[end]);
}

void updateOccupiedHandler(const httplib::Request& req, httplib::Response& res) {
    try {
        json j = json::parse(req.body);
        std::string id = j["id"];
        int occupied = j["occupied"];

        auto it = points.find(id);
        if (it != points.end()) {
            it->second.Occupied = occupied;
            res.status = 200;
            res.set_content("Updated", "text/plain");
        } else {
            res.status = 404;
            res.set_content("Point not found", "text/plain");
        }
    } catch (const std::exception& e) {
        res.status = 400;
        res.set_content("invalid request", "text/plain");
    }
}

struct Location {
    double Lat;
    double Lng;
    
    Location() : Lat(0.0), Lng(0.0) {}
    Location(double lat, double lng) : Lat(lat), Lng(lng) {}
};

// Convert JSON to Location
void from_json(const json& j, Location& l) {
    j.at("lat").get_to(l.Lat);
    j.at("lng").get_to(l.Lng);
}

double Haversine(double lat1, double lon1, double lat2, double lon2) {
    const double R = 6371e3; // bán kính Trái đất (m)
    double phi1 = lat1 * M_PI / 180;
    double phi2 = lat2 * M_PI / 180;
    double deltaphi = (lat2 - lat1) * M_PI / 180;
    double deltalamda = (lon2 - lon1) * M_PI / 180;

    double a = std::sin(deltaphi/2) * std::sin(deltaphi/2) +
               std::cos(phi1) * std::cos(phi2) *
               std::sin(deltalamda/2) * std::sin(deltalamda/2);
    double c = 2 * std::atan2(std::sqrt(a), std::sqrt(1-a));

    return R * c; // khoảng cách (mét)
}

std::string FindClosestNodeFromLocation(const Location& loc) {
    double minDist = std::numeric_limits<double>::max();
    std::string closest = "";
    
    for (const auto& p : points) {
        // Chỉ chọn điểm có trong đồ thị (có thể lọc qua graph[id])
        if (graph.find(p.first) != graph.end()) {
            double dist = Haversine(loc.Lat, loc.Lng, p.second.Lat, p.second.Lng);
            if (dist < minDist) {
                minDist = dist;
                closest = p.first;
            }
        }
    }
    return closest;
}

std::pair<std::string, double> FindNearestPoint(const Location& current) {
    double minDist = std::numeric_limits<double>::max();
    std::string nearest = "";

    for (const auto& p : points) {
        double dist = Haversine(current.Lat, current.Lng, p.second.Lat, p.second.Lng);
        if (dist < minDist) {
            minDist = dist;
            nearest = p.first;
        }
    }

    return std::make_pair(nearest, minDist);
}

// Tìm nhà xe gần nhất (còn chỗ) có tổng số đường đi bé nhất với point truyền vào (theo graph)
std::string FindNearestAvailableParking(const std::string& fromID) {
    int minDist = std::numeric_limits<int>::max();
    std::string nearest = "";
    
    for (const auto& p : points) {
        // Bỏ qua các điểm không phải nhà xe hoặc đã đầy
        if (p.first.find("Nha xe") == std::string::npos || 
            p.second.Capacity == 0 || 
            p.second.Occupied >= p.second.Capacity) {
            continue;
        }
        
        // Tìm đường đi ngắn nhất từ fromID đến id
        auto result = Dijkstra(graph, fromID, p.first);
        if (result.second < 0) continue; // Skip if no path
        
        if (result.second < minDist) {
            minDist = result.second;
            nearest = p.first;
        }
    }
    
    if (nearest.empty()) {
        // Fallback: return any available parking
        for (const auto& p : points) {
            if (p.first.find("Nha xe") != std::string::npos && 
                p.second.Capacity > 0 && 
                p.second.Occupied < p.second.Capacity) {
                return p.first;
            }
        }
    }
    
    return nearest;
}
void setCORS(httplib::Response& res) {
    res.set_header("Access-Control-Allow-Origin", "*");
    res.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    res.set_header("Access-Control-Allow-Headers", "Content-Type");
}

int main() {
    httplib::Server server;
    
    // Biến lưu trữ sinh viên (tải từ file khi khởi động)
    // std::unordered_map<std::string, Student> students = LoadStudents();
     // Tải dữ liệu khi khởi động
    auto students = LoadStudents();
    auto parkingLots = LoadParkingLots();
    auto parkingHistory = LoadParkingHistory();



    // API thêm sinh viên mới
    server.Post("/students", [&students](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        try {
            json j = json::parse(req.body);
            Student s;
            s.id = j["id"].get<std::string>();
            s.name = j["name"].get<std::string>();
            s.faculty = j["faculty"].get<std::string>();
            s.licensePlate = j["licensePlate"].get<std::string>();
            
            if (students.find(s.id) != students.end()) {
                res.status = 400;
                res.set_content(json{{"error", "Student ID already exists"}}.dump(), "application/json");
                return;
            }
            
            students[s.id] = s;
            SaveStudents(students);
            
            res.status = 201;
            res.set_content(json{{"message", "Student added successfully"}, {"id", s.id}}.dump(), "application/json");
        } catch (const std::exception& e) {
            res.status = 400;
            res.set_content(json{{"error", "Invalid student data"}}.dump(), "application/json");
        }
    });

    // API lấy thông tin sinh viên
       // API thêm sinh viên mới
    server.Post("/students", [&students](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        try {
            json j = json::parse(req.body);
            Student s;
            s.id = j["id"].get<std::string>();
            s.name = j["name"].get<std::string>();
            s.faculty = j["faculty"].get<std::string>();
            s.licensePlate = j["licensePlate"].get<std::string>();
            
            if (students.find(s.id) != students.end()) {
                res.status = 400;
                res.set_content(json{{"error", "Student ID already exists"}}.dump(), "application/json");
                return;
            }
            
            students[s.id] = s;
            SaveStudents(students);
            
            res.status = 201;
            res.set_content(json{{"message", "Student added successfully"}, {"id", s.id}}.dump(), "application/json");
        } catch (const std::exception& e) {
            res.status = 400;
            res.set_content(json{{"error", "Invalid student data"}}.dump(), "application/json");
        }
    });

    // API lấy thông tin sinh viên
    server.Get("/students/:id", [&students](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        std::string id = req.path_params.at("id");
        
        auto it = students.find(id);
        if (it != students.end()) {
            json j = it->second;
            res.set_content(j.dump(), "application/json");
        } else {
            res.status = 404;
            res.set_content(json{{"error", "Student not found"}}.dump(), "application/json");
        }
    });

    // API cập nhật thông tin sinh viên
    server.Put("/students/:id", [&students](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        try {
            std::string id = req.path_params.at("id");
            json j = json::parse(req.body);
            
            if (students.find(id) == students.end()) {
                res.status = 404;
                res.set_content(json{{"error", "Student not found"}}.dump(), "application/json");
                return;
            }
            
            Student& s = students[id];
            if (j.contains("name")) s.name = j["name"];
            if (j.contains("faculty")) s.faculty = j["faculty"];
            if (j.contains("licensePlate")) s.licensePlate = j["licensePlate"];
            
            SaveStudents(students);
            res.set_content(json{{"message", "Student updated successfully"}}.dump(), "application/json");
        } catch (const std::exception& e) {
            res.status = 400;
            res.set_content(json{{"error", "Invalid student data"}}.dump(), "application/json");
        }
    });

    // API xóa sinh viên
    server.Delete("/students/:id", [&students](const httplib::Request& req, httplib::Response& res) {
       setCORS(res);
        std::string id = req.path_params.at("id");
        
        if (students.erase(id)) {
            SaveStudents(students);
            res.set_content(json{{"message", "Student deleted successfully"}}.dump(), "application/json");
        } else {
            res.status = 404;
            res.set_content(json{{"error", "Student not found"}}.dump(), "application/json");
        }
    });

    // API lấy danh sách tất cả sinh viên
    server.Get("/students", [&students](const httplib::Request&, httplib::Response& res) {
       setCORS(res);
        json j;
        for (const auto& pair : students) {
            j.push_back(pair.second);
        }
        res.set_content(j.dump(), "application/json");
    });

    // API lấy trạng thái các nhà xe
    server.Get("/parking-status", [&parkingLots](const httplib::Request&, httplib::Response& res) {
        setCORS(res);
        json j;
        for (const auto& pair : parkingLots) {
            const ParkingLot& p = pair.second;
            json parking = {
                {"name", p.name},
                {"capacity", p.capacity},
                {"occupied", p.occupied},
                {"available", p.capacity - p.occupied}
            };
            j.push_back(parking);
        }
        res.set_content(j.dump(), "application/json");
    });

    // API tìm kiếm thông tin thẻ xe
    server.Get("/card-info", [&students](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        std::string search = req.get_param_value("search");
        
        // Tìm theo ID sinh viên hoặc biển số xe
        for (const auto& pair : students) {
            const Student& s = pair.second;
            if (s.id == search || s.licensePlate == search) {
                json response = {
                    {"studentId", s.id},
                    {"studentName", s.name},
                    {"licensePlate", s.licensePlate},
                    {"balance", s.balance},
                    {"transactions", s.transactions}
                };
                res.set_content(response.dump(), "application/json");
                return;
            }
        }
        
        res.status = 404;
        res.set_content(json{{"error", "Card not found"}}.dump(), "application/json");
    });

    // API nạp tiền vào thẻ xe
    server.Post("/top-up", [&students](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        try {
            json j = json::parse(req.body);
            std::string studentId = j["studentId"];
            double amount = j["amount"];
            
            auto it = students.find(studentId);
            if (it == students.end()) {
                res.status = 404;
                res.set_content(json{{"error", "Student not found"}}.dump(), "application/json");
                return;
            }
            
            Student& s = it->second;
            s.balance += amount;
            
            // Thêm giao dịch
            std::string transaction = currentDateTime() + " - Nạp tiền: +" + 
                                      std::to_string(amount) + " VND";
            s.transactions.push_back(transaction);
            
            SaveStudents(students);
            
            res.set_content(json{
                {"message", "Top-up successful"},
                {"newBalance", s.balance}
            }.dump(), "application/json");
            
        } catch (const std::exception& e) {
            res.status = 400;
            res.set_content(json{{"error", "Invalid request"}}.dump(), "application/json");
        }
    });


    // API lấy trạng thái các nhà xe
    server.Get("/parking-status", [](const httplib::Request&, httplib::Response& res) {
       setCORS(res); 
        json j;
        for (const auto& p : points) {
            if (p.first.find("Nha xe") != std::string::npos) {
                json parking = {
                    {"name", p.first},
                    {"capacity", p.second.Capacity},
                    {"occupied", p.second.Occupied},
                    {"available", p.second.Capacity - p.second.Occupied}
                };
                j.push_back(parking);
            }
        }
        res.set_content(j.dump(), "application/json");
    });

    // API tìm kiếm thông tin thẻ xe
    server.Get("/card-info", [&students](const httplib::Request& req, httplib::Response& res) {
      setCORS(res); 
        std::string search = req.get_param_value("search");
        
        // Tìm theo ID sinh viên hoặc biển số xe
        for (const auto& pair : students) {
            const Student& s = pair.second;
            if (s.id == search || s.licensePlate == search) {
                json response = {
                    {"studentId", s.id},
                    {"studentName", s.name},
                    {"licensePlate", s.licensePlate},
                    {"balance", s.balance},
                    {"transactions", s.transactions}
                };
                res.set_content(response.dump(), "application/json");
                return;
            }
        }
        
        res.status = 404;
        res.set_content(json{{"error", "Card not found"}}.dump(), "application/json");
    });

    // API nạp tiền vào thẻ xe
    server.Post("/top-up", [&students](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        try {
            json j = json::parse(req.body);
            std::string studentId = j["studentId"];
            double amount = j["amount"];
            
            auto it = students.find(studentId);
            if (it == students.end()) {
                res.status = 404;
                res.set_content(json{{"error", "Student not found"}}.dump(), "application/json");
                return;
            }
            
            Student& s = it->second;
            s.balance += amount;
            
            // Thêm giao dịch
            std::string transaction = currentDateTime() + " - Nạp tiền: +" + 
                                      std::to_string(amount) + " VND";
            s.transactions.push_back(transaction);
            
            SaveStudents(students);
            
            res.set_content(json{
                {"message", "Top-up successful"},
                {"newBalance", s.balance}
            }.dump(), "application/json");
            
        } catch (const std::exception& e) {
            res.status = 400;
            res.set_content(json{{"error", "Invalid request"}}.dump(), "application/json");
        }
    });

 server.Get("/report", [&](const httplib::Request& req, httplib::Response& res) {
    setCORS(res);
    // Lấy tham số
    std::string parking = req.get_param_value("parking");
    std::string fromDate = req.get_param_value("from");
    std::string toDate = req.get_param_value("to");
    
    // Tải lại lịch sử để có dữ liệu mới nhất
    auto history = LoadParkingHistory();
    
    json report;
    
    // Tạo bản đồ tổng hợp
    std::unordered_map<std::string, json> parkingReports;
    
    // Khởi tạo dữ liệu cho từng bãi xe
    for (const auto& pair : parkingLots) {
        const std::string& name = pair.first;
        parkingReports[name] = {
            {"parkingName", name},
            {"entryCount", 0},
            {"exitCount", 0},
            {"revenue", 0.0},
            {"usageRate", 0.0}
        };
    }
    
    // Xử lý từng bản ghi lịch sử
    for (const auto& record : history) {
        // Kiểm tra bãi xe
        if (!parking.empty() && parking != "all" && record.parkingLot != parking) {
            continue;
        }
        
        // Kiểm tra thời gian
        if (!fromDate.empty()) {
            time_t entryTime = stringToTime(record.entryTime);
            time_t fromTime = stringToTime(fromDate);
            if (entryTime < fromTime) continue;
        }
        
        if (!toDate.empty()) {
            time_t entryTime = stringToTime(record.entryTime);
            time_t toTime = stringToTime(toDate);
            if (entryTime > toTime) continue;
        }
        
        // Cập nhật báo cáo
        auto& reportData = parkingReports[record.parkingLot];
        reportData["entryCount"] = reportData["entryCount"].get<int>() + 1;
        
        if (!record.exitTime.empty()) {
            reportData["exitCount"] = reportData["exitCount"].get<int>() + 1;
            reportData["revenue"] = reportData["revenue"].get<double>() + record.fee;
        }
    }
    
    // Tính tỉ lệ sử dụng và thêm vào kết quả
    for (auto& pair : parkingReports) {
        auto& reportData = pair.second;
        std::string name = reportData["parkingName"];
        
        if (parkingLots.find(name) != parkingLots.end()) {
            int capacity = parkingLots[name].capacity;
            int entryCount = reportData["entryCount"];
            
            if (capacity > 0) {
                double usageRate = (static_cast<double>(entryCount) / capacity) * 100;
                reportData["usageRate"] = usageRate;
            }
        }
        
        report.push_back(reportData);
    }
        res.set_content(report.dump(), "application/json");

    // Tạo thư mục Report nếu chưa tồn tại
    #ifdef _WIN32
        _mkdir("Report");
    #else
        mkdir("Report", 0777);
    #endif

    // Lấy thời gian hiện tại để đặt tên file
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&in_time_t), "%Y%m%d_%H%M%S");
    std::string filename = "Report/" + ss.str() + ".json";

    // Lưu báo cáo ra file
    std::ofstream outFile(filename);
    outFile << report.dump(4);
    outFile.close();

  
});

    // Serve static files
    server.set_mount_point("/", "./public");
    
    // Default route - serve index.html
    server.Get("/", [](const httplib::Request&, httplib::Response& res) {
        setCORS(res);
        std::ifstream file("./index.html");
        if (file) {
            std::stringstream buffer;
            buffer << file.rdbuf();
            res.set_content(buffer.str(), "text/html");
        } else {
            res.status = 404;
            res.set_content("File not found", "text/plain");
        }
    });


    // API lấy đường đi
    server.Get("/path", [](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        std::string from = req.get_param_value("from");
        std::string to = req.get_param_value("to");
        
        auto result = Dijkstra(graph, from, to);
        std::vector<std::string> path = result.first;
        
        std::vector<Coordinate> coordinates;
        for (const std::string& id : path) {
            auto it = points.find(id);
            if (it != points.end()) {
                const Point& p = it->second;
                coordinates.push_back(Coordinate(p.Lat, p.Lng));
            }
        }
        
        json j = coordinates;
        res.set_content(j.dump(), "application/json");
    });

    // API cập nhật số xe đang đỗ
    server.Post("/update-occupied", [](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        updateOccupiedHandler(req, res);
    });

    // API tìm nhà xe gần nhất còn chỗ
    server.Post("/nearest", [](const httplib::Request& req, httplib::Response& res) {
        setCORS(res);
        try {
            json j = json::parse(req.body);
            Location loc;
            from_json(j, loc);
            
            auto nearestResult = FindNearestPoint(loc);
            std::string nearestPointID = nearestResult.first;
            
            if (nearestPointID.empty()) {
                json errorResponse = {{"error", "no available parking"}};
                res.status = 404;
                res.set_content(errorResponse.dump(), "application/json");
                return;
            }

            std::string nearestParkingID = FindNearestAvailableParking(nearestPointID);
            if (nearestParkingID.empty()) {
                json errorResponse = {{"error", "no available parking"}};
                res.status = 404;
                res.set_content(errorResponse.dump(), "application/json");
                return;
            }

            auto pathResult = Dijkstra(graph, nearestPointID, nearestParkingID);
            std::vector<std::string> path = pathResult.first;

            std::vector<Coordinate> coordinates;
            for (const std::string& id : path) {
                auto it = points.find(id);
                if (it != points.end()) {
                    const Point& p = it->second;
                    coordinates.push_back(Coordinate(p.Lat, p.Lng));
                }
            }
            
            json response = {
                {"parkingID", nearestParkingID},
                {"path", coordinates}
            };
            res.set_content(response.dump(), "application/json");
        } catch (const std::exception& e) {
            json errorResponse = {{"error", "invalid location"}};
            res.status = 400;
            res.set_content(errorResponse.dump(), "application/json");
        }
    });

    // Serve static files
    server.set_mount_point("/", "./public");
    
    // Default route - serve index.html
    server.Get("/", [](const httplib::Request&, httplib::Response& res) {
        setCORS(res);
        std::ifstream file("./index.html");
        if (file) {
            std::stringstream buffer;
            buffer << file.rdbuf();
            res.set_content(buffer.str(), "text/html");
        } else {
            res.status = 404;
            res.set_content("File not found", "text/plain");
        }
    });

    std::cout << "Server starting on port 8080..." << std::endl;
    server.listen("0.0.0.0", 8080);

    return 0;
}
