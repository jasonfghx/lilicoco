#include <stdio.h>
#include <cstdlib>
#include <utility>
#include <direct.h>
#include <memory>
#include <pybind11.h>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <fstream>
#include <regex>
#include <sstream>
#include <string>
#include <vector>
#include <list>
#include <stl.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct Point {
    double x, y;
} Point;

typedef struct Eq_Line {
    double c1, c2, c3;
} Eq_Line;

typedef struct Eq_Circle {
    // ciecle_eq = x^2+y^2+dx+ey+f=0
    double d, e, f;
} Eq_Circle;

typedef struct Hit_Angle {
    int degree;
} Hit_Angle;

typedef struct Ans {
    Point p1, p2;
} Ans;

typedef struct Region {
    double x_min, x_max, y_min, y_max;
} Region;
//-------------------------------------------------------

class loop_iterator {
public:
    loop_iterator(std::list<Hit_Angle>& lst, bool is_end = false) : lst_(lst) {
        it_ = is_end ? std::prev(lst.end()) : lst.begin();
    }

    Hit_Angle& operator*() { return *it_; }

    loop_iterator& operator++() {
        ++it_;
        if (it_ == lst_.end()) {
            it_ = lst_.begin();
        }
        return *this;
    }

    loop_iterator& operator--() {
        if (it_ == lst_.begin()) {
            it_ = std::prev(lst_.end());
        }
        else {
            --it_;
        }
        return *this;
    }

    bool operator==(const loop_iterator& other) const { return it_ == other.it_; }

    bool operator!=(const loop_iterator& other) const {
        return !(*this == other);
    }

    loop_iterator prev() {
        loop_iterator temp = *this;
        --temp;
        return temp;
    }

    loop_iterator next() {
        loop_iterator temp = *this;
        ++temp;
        return temp;
    }

private:
    std::list<Hit_Angle>& lst_;
    std::list<Hit_Angle>::iterator it_;
};

//-------------Shape---------------------------------------
class Shape {
public:
    virtual Point hit(Point in1, Point in2) = 0;
    virtual void print_out() = 0;
    virtual std::vector<double> get_data() = 0;
    std::vector<Point> get_extreme() { return exterme; }
    double leng = 0;

protected:
    Region shape_region = { 0, 0, 0, 0 };
    std::vector<Point> exterme;
};
//--------------Line----------------------------------------

class Line : public Shape {
public:
    Line() = default;  // for python

    Line(double x1, double y1, double x2, double y2) {
        Point p1 = { x1, y1 };
        Point p2 = { x2, y2 };
        Point v = { x2 - x1, y2 - y1 };
        this->p1 = p1;
        this->p2 = p2;
        this->v = v;

        this->exterme.push_back(p1);
        this->exterme.push_back(p2);

        this->shape_region.x_min = std::min(x1, x2);
        this->shape_region.x_max = std::max(x1, x2);
        this->shape_region.y_min = std::min(y1, y2);
        this->shape_region.y_max = std::max(y1, y2);

        this->leng = length();
    }

    Line(Point a, Point b) {
        Point v = { b.x - a.x, b.y - a.y };
        this->p1 = a;
        this->p2 = b;
        this->v = v;

        double x_min = std::min(p1.x, p2.x);
        double x_max = std::max(p1.x, p2.x);

        double y_min = std::min(p1.y, p2.y);
        double y_max = std::max(p1.y, p2.y);

        this->shape_region.x_min = x_min;
        this->shape_region.x_max = x_max;
        this->shape_region.y_min = y_min;
        this->shape_region.y_max = y_max;

        this->exterme.push_back(p1);
        this->exterme.push_back(p2);

        this->leng = length();
    }

    Eq_Line find_Eq_Line() {
        double m = find_slope();
        double c = p1.y - m * p1.x;

        Eq_Line result = { 0, 0,0 };

        if (m == INFINITY) {
            result.c1 = 1;
            result.c2 = 0;
            result.c3 = -(p1.x);
        }
        else {
            result.c1 = m;
            result.c2 = -1;
            result.c3 = c;
        }
        return result;
    }

    double find_slope() {
        if (v.x == 0) {
            return INFINITY;
        }
        else {
            return (v.y) / (v.x);
        }
    }

    Point midpoint() {
        Point p = { (p2.x + p1.x) / 2, (p2.y + p1.y) / 2 };
        return p;
    }

    double length() { return pow(pow(v.x, 2) + pow(v.y, 2), 0.5); }

    double distance_point2line(Point input) {
        Eq_Line coeff = find_Eq_Line();
        return fabs(coeff.c1 * input.x + coeff.c2 * input.y + coeff.c3) /
            pow(pow(coeff.c1, 2) + pow(coeff.c2, 2), 0.5);
    }

    bool inside(Point check) {
        /*
        double x = round(check.x * 10000) / 10000;
        double y = round(check.y * 10000) / 10000;

        double x_min = round(shape_region.x_min * 10000) / 10000;
        double y_min = round(shape_region.y_min * 10000) / 10000;
        double x_max = round(shape_region.x_max * 10000) / 10000;
        double y_max = round(shape_region.y_max * 10000) / 10000;*/
    
        double x = check.x;
        double y =check.y;

        double x_min = shape_region.x_min;
        double y_min = shape_region.y_min ;
        double x_max = shape_region.x_max;
        double y_max =shape_region.y_max ;

        if ( x_min<= x && x <= x_max &&
            y_min <= y && y <= y_max) {
            return true;
        }
        else {
            return false;
        }
    }

    Point univector() {
        Point a = { v.x / leng, v.y / leng };
        return a;
    }

    double det(double x1, double y1, double x2, double y2) {
        return x1 * y2 - x2 * y1;
    }

    double cross(Point v2) { return v.x * v2.y - v.y * v2.x; }

    double dot_line(Line v2) { return v.x * v2.v.x + v.y * v2.v.y; }

    double angle_btw_line(Line v2) { 

        double dot_result=dot_line(v2);
        double cos_angle = dot_result / (v2.leng * leng);
        if (cos_angle > 1.0) {
            cos_angle = 1.0;
        }
        else if (cos_angle < -1.0) {
            cos_angle = -1.0;
        }
        double angle = std::acos(cos_angle) * (180 / M_PI);
        return angle;
    }

    Point getter(char name) {
        Point n = { 0, 0 };
        switch (name) {
        case '1':
            n = p1;
            break;
        case '2':
            n = p2;
            break;
        case 'v':
            n = v;
            break;
        }
        return n;
    }

    Point hit(Point in1, Point in2) {
        Line check(in1, in2);
        Point v2 = check.getter('v');

        Point temp = p1;

        Point none = { NAN, NAN };

        Line ll3(p1, in1);

        if (cross(v2) == 0) {
            return none;
        }
        else if (v2.x == 0) {  // 若 check 為垂直線
            double dett = (in1.x - p1.x) / v.x;
            Point section_point = { in1.x, p1.y + v.y * dett };

            if (inside(section_point) && check.inside(section_point)) {
                return section_point;
            }
            return none;
        }
        else if (v2.y == 0) {  // 若 check 為水平線
            double dett = (in1.y - p1.y) / v.y;
            Point section_point = { p1.x + v.x * dett, in1.y };

            if (inside(section_point) && check.inside(section_point)) {
                return section_point;
            }
            return none;
        }
        else {
            double dett = ll3.cross(v2) / cross(v2);

            Point a1 = getter('1');

            Point section_point = { a1.x + v.x * dett, a1.y + v.y * dett };

            if (inside(section_point) && check.inside(section_point)) {
                return section_point;
            }
            return none;
        }
    }

    Line rotate(double angle) {
        double coss = 0.0, sinn = 0.0;

        if (angle >= 360) {
            double cc = angle / 360;
            angle = angle - int(cc) * 360;
        }

        if (angle == 90.0) {
            coss = 0.0;
            sinn = 1.0;
        }
        else if (angle == 180.0) {
            coss = -1.0;
            sinn = 0.0;
        }
        else if (angle == 270.0) {
            coss = 0.0;
            sinn = -1.0;
        }
        else {
            angle = angle * (M_PI / 180);
            coss = cos(angle);
            sinn = sin(angle);
        }

        Point v_new = { v.x * coss - v.y * sinn, v.x * sinn + v.y * coss };
        Point b_new = { p1.x + v_new.x, p1.y + v_new.y };
        Point a_new = { p1.x, p1.y };

        Line temp(a_new, b_new);
        return temp;
    }

    void print_out() {
        printf("Line: %.2f, %.2f, %.2f, %.2f\t v:%.2f, %.2f\n", p1.x, p1.y, p2.x,
            p2.y, v.x, v.y);
    }

    std::vector<double> get_data() {
        std::vector<double> data = { p1.x, p1.y, p2.x, p2.y };
        return data;
    }

    std::vector<double> get_v() {
        std::vector<double> data = { v.x,v.y };
        return data;
    }

private:
    Point p1, p2;
    Point v;
};

//-------------Poly------------------------------------------

class Poly : public Shape {
public:
    Poly() = default;  // for python

    Poly(std::vector<double> input) {
        std::vector<Point> input_points;
        std::vector<double> xs, ys;
        std::vector<Line> lines;

        for (int k = 0; k < input.size(); k += 2) {
            Point each_point = { input[k], input[k + 1] };
            input_points.push_back(each_point);
        }
        input_points.push_back(input_points[0]);

        for (const auto p : input_points) {
            xs.push_back((p).x);
            ys.push_back((p).y);
        }

        auto max_x = std::max_element(xs.begin(), xs.end());
        auto max_y = std::max_element(ys.begin(), ys.end());
        auto min_x = std::min_element(xs.begin(), xs.end());
        auto min_y = std::min_element(ys.begin(), ys.end());

        for (int i = 0; i < input_points.size() - 1; i++) {
            Line p(input_points[i], input_points[i + 1]);
            lines.push_back(p);
        }

        this->lines = lines;
        this->xs = xs;
        this->ys = ys;
        this->data = input;

        this->shape_region.x_min = *min_x;
        this->shape_region.x_max = *max_x;
        this->shape_region.y_min = *min_y;
        this->shape_region.y_max = *max_y;

        Point ld = { *min_x, *min_y };
        Point rd = { *max_x, *min_y };
        Point ru = { *max_x, *max_y };
        Point lu = { *min_x, *max_y };

        Line diagonal1(ld, ru);
        Line diagonal2(lu, rd);
        if (diagonal1.leng >= diagonal2.leng) {
            this->exterme.push_back(diagonal1.midpoint());
            this->leng = diagonal1.leng / 2;
        }
        else {
            this->exterme.push_back(diagonal2.midpoint());
            this->leng = diagonal2.leng / 2;
        }
    }

    Point hit(Point in1, Point in2) {
        Line check(in1, in2);
        std::vector<Point> hit_list;
        std::vector<double> d_list;

        double length_line = check.length();
        Point start_point = check.getter('1');

        Point a = { NAN, NAN };

        for (auto it = lines.begin(); it != lines.end(); ++it) {
            Point ann = check.hit((*it).getter('1'), (*it).getter('2'));

            if (!std::isnan(ann.x) && !std::isnan(ann.y)) {
                hit_list.push_back(ann);

                Line temp(check.getter('1'), ann);
                double d = temp.length();

                d_list.push_back(d);
            }
        }

        if (hit_list.empty()) {
            return a;
        }
        else {
            auto min = min_element(d_list.begin(), d_list.end());
            auto index = distance(d_list.begin(), min);

            return hit_list[index];
        }
    }

    double distance_between_points(Point a, Point b) {
        return pow(pow(b.x - a.x, 2) + pow(b.y - a.y, 2), 0.5);
    }

    void print_out() {
        printf("Polys:");
        int i = 0;
        for (double it : data) {
            if (i % 2 == 0) {
                printf("[");
            }

            printf("%.2f, ", it);

            if (i % 2 == 1) {
                printf("]");
            }
            i++;
        }
        printf("\n");
    }

    std::vector<double> get_data() { return data; }

    std::vector<double> get_xdata() { return xs; }

    std::vector<double> get_ydata() { return ys; }

private:
    std::vector<Line> lines;
    std::vector<double> xs, ys, data;
    // shape:Region shape_region = { 0,0 ,0,0 };
};

//-----------Circle-----------------------------------------
class Circle : public Shape {
public:
    Circle() = default;  // for python

    Circle(double a, double b, double c) {
        this->r = a;
        Point center = { b, c };
        this->center = center;
        this->exterme.push_back(center);
        this->leng = r;
    }

    double distance_2_center(Point p) {
        Line temp(center, p);
        return temp.length();
    }

    Eq_Circle find_eq() {
        Eq_Circle eq = { (center.x) * -2, (center.y) * -2,
                        (pow(center.x, 2) + pow(center.y, 2) - pow(r, 2)) };
        return eq;
    }

    Point solve_quadratic_eq(Eq_Line eq) {
        double a = eq.c1, b = eq.c2, c = eq.c3;

        double key = pow(b, 2) - 4 * a * c;

        Point ans;

        if (key > 0) {
            ans = { (-b + sqrt(key)) / (2 * a), (-b - sqrt(key)) / (2 * a) };

        }
        else if (key == 0) {
            double temp = (-b + sqrt(key)) / (2 * a);
            ans = { temp, temp };

        }
        else {
            ans = { NAN, NAN };
        }
        return ans;
    }

    Point hit(Point in1, Point in2) {
        Line check(in1, in2);
        Point ans_return = { NAN, NAN };

        Eq_Line coeff = check.find_Eq_Line();
        Eq_Circle c_coeff = find_eq();
        double m = check.find_slope();
        double delta = check.distance_point2line(center);

        double aa, bb, cc;
        if (m == INFINITY) {
            aa = 1;
            bb = c_coeff.e;
            cc = pow(coeff.c3, 2) - coeff.c3 * c_coeff.d + c_coeff.f;
        }
        else {
            aa = (pow(m, 2) + 1);
            bb = c_coeff.d + c_coeff.e * m + 2 * m * coeff.c3;
            cc = c_coeff.e * coeff.c3 + c_coeff.f + pow(coeff.c3, 2);
        }

        Eq_Line qu_coeff = { aa, bb, cc };
        Ans ans = { 0, 0, 0 };

        if (delta >= r) {
            return ans_return;

        }
        else {
            Point qu_ans = solve_quadratic_eq(qu_coeff);

            if (m == INFINITY) {
                ans.p1.x = -coeff.c3;
                ans.p1.y = qu_ans.x;
                ans.p2.x = -coeff.c3;
                ans.p2.y = qu_ans.y;
            }
            else {
                ans.p1.x = qu_ans.x;
                ans.p1.y = m * qu_ans.x + coeff.c3;
                ans.p2.x = qu_ans.y;
                ans.p2.y = m * qu_ans.y + coeff.c3;
            }

            Point p1_check = check.getter('1');

            Line temp1(p1_check, ans.p1);
            double distance_p1 = temp1.length();

            Line temp2(p1_check, ans.p2);
            double distance_p2 = temp2.length();

            if (distance_p1 < distance_p2 && check.inside(ans.p1)) {
                return ans.p1;
            }
            else if (check.inside(ans.p2)) {
                return ans.p2;
            }
            else {
                return ans_return;
            }
        }
    }

    bool in_region(Shape* check) {
        std::vector<Point> check_extreme = check->get_extreme();

        if (typeid(*check) == typeid(Line)) {
            Line temp(check_extreme[0], check_extreme[1]);
            double d = temp.distance_point2line(center);
            if (d <= r) {
                return true;
            }
            else {
                return false;
            }
        }
        if (typeid(*check) == typeid(Circle)|| typeid(*check) == typeid(Poly)) {
            double d = distance_2_center(check_extreme[0]);
            if (d <= r + check->leng) {
                return true;
            }
            else {
                return false;
            }
        }
        throw std::runtime_error("Something went wrong");
    }

    bool py_inregion(Circle check) {
        Shape* temp = &check;
        bool result=in_region(temp);
        return result;

    }

    bool point_inside_range(double x, double y) {
        Line temp(center.x, center.y, x, y);
        if (temp.length() <= r) {
            return true;
        }
        else {
            return false;
        }
    }

    Point project_to_circle(double x, double y) {
        Point end = {x,y};
        Line line(center, end);
        Point new_vector = line.univector();
        new_vector.x *= r;
        new_vector.x += center.x;
        new_vector.y *= r;
        new_vector.y += center.y;
        return new_vector;
    }

    std::vector<double> get_data() {
        std::vector<double> datas = { r, center.x, center.y };
        return datas;
    }

    void print_out() {
        printf("Circle: %.2f. %.2f, %.2f \n", r, center.x, center.y);
    }

private:
    double r;
    Point center;
};

//---------vector_map----------------------------------------
class Vector_map {
public:
    Vector_map() {
        std::vector<std::pair<double, double>> local_scan_result(3600);
        std::list<Hit_Angle> local_scan_result_area(3600);
        this->scan_result= local_scan_result;
        this->scan_result_area= local_scan_result_area;
    }
    void readfile(std::string path, std::string path_type) {
        this->size[0] = 0;
        this->size[1] = 0;
        this->shape_num[0] = 0;
        this->shape_num[1] = 0;

        char* buffer = nullptr;
        if ((buffer = _getcwd(NULL, 0)) != NULL) {
            printf("Current working directory: %s\n", buffer);
        }
        else {
            perror("_getcwd() error");
            throw std::runtime_error("Read file error!\n");
        }

        if (path_type == "relative") {
            path = std::string(buffer) + "\\map_files\\" + path;
        }
        free(buffer);
        std::ifstream fp(path);

        if (fp.is_open()) {
            std::string line;
            while (getline(fp, line)) {
                if (line.find("size") != std::string::npos) {
                    std::regex reg("-?\\d+(\\.\\d+)?");
                    std::sregex_iterator it(line.begin(), line.end(), reg);
                    std::sregex_iterator end;
                    double size[2] = { 0, 0 };
                    int i = 0;
                    while (it != end) {
                        size[i++] = std::stod(it->str());
                        ++it;
                    }
                    create_border(size[0], size[1]);
                }
                if (line.find("poly") != std::string::npos) {
                    std::regex reg("-?\\d+(\\.\\d+)?");
                    std::sregex_iterator it(line.begin(), line.end(), reg);
                    std::sregex_iterator end;
                    std::vector<double> points;

                    while (it != end) {
                        points.push_back(std::stod(it->str()));
                        ++it;
                    }
                    create_poly(points);
                }
                if (line.find("circle") != std::string::npos) {
                    std::regex reg("-?\\d+(\\.\\d+)?");
                    std::sregex_iterator it(line.begin(), line.end(), reg);
                    std::sregex_iterator end;

                    int i = 0;

                    double para[3] = { 0 };

                    while (it != end) {
                        para[i++] = std::stod(it->str());
                        ++it;
                    }
                    create_circle(para[0], para[1], para[2]);
                }
                if (line.find("\t#") != std::string::npos ||
                    line.find("\t\t#") != std::string::npos) {
                    add_note(line);
                }
            }

        }
        else {
            printf("input file opening failed\n");
            exit(1);
        }

        fp.close();
    }

    ~Vector_map() {
        for (Shape* it : myshapes) {
            delete it;
        }
    }

    void create_border(double x, double y) {
        this->size[0] = x;
        this->size[1] = y;
        Line* l = new Line(0, 0, 0, y);
        Line* r = new Line(x, 0, x, y);
        Line* u = new Line(0, y, x, y);
        Line* d = new Line(0, 0, x, 0);

        this->myshapes.push_back(d);
        this->myshapes.push_back(r);
        this->myshapes.push_back(u);
        this->myshapes.push_back(l);
    }

    void create_poly(const std::vector<double> in) {
        Poly* new_one = new Poly(in);
        this->myshapes.push_back(new_one);
        this->shape_num[0]++;
    }

    void create_circle(double a, double b, double c) {
        Circle* new_one = new Circle(a, b, c);
        this->myshapes.push_back(new_one);
        this->shape_num[1]++;
    }

    void add_note(const std::string in) { this->mynote.push_back(in); }

    void print_out_data() {
        for (Shape* it : myshapes) {
            it->print_out();
        }
    }

    void delete_shape() {
        Shape* last_element = myshapes.back();
        delete last_element;
        this->myshapes.pop_back();
    }

    int get_shape_num(int name) { return shape_num[name]; }

    std::vector<Shape*> get_shape_list() { return std::vector<Shape*>(myshapes); }

    bool scan_one_line(const double curr_x, const double curr_y,const double lidar_r, const double end_x, const double end_y) {
        Line line(curr_x, curr_y, end_x, end_y);
        const Point curr = { curr_x, curr_y };
        Circle lidar_range(lidar_r, curr_x, curr_y);
        if (!lidar_range.point_inside_range(end_x, end_y)) {
            return true;
        }


        for (Shape* it : myshapes) {
            if (lidar_range.in_region(it)) {
                Point hit = (it)->hit(line.getter('1'),line.getter('2'));

                if (std::isnormal(hit.x) && std::isnormal(hit.y) &&
                    lidar_range.point_inside_range(hit.x, hit.y)) {
                    
                    return true;
                }
            }
            else {
                continue;
            }
        }
        return false;

    }

    void scan(const double curr_x, const double curr_y, const double radius,
        const int max_angle, const char type) {
        Line line(curr_x, curr_y, curr_x + radius, curr_y);
        const Point curr = { curr_x, curr_y };
        Circle lidar_range(radius, curr_x, curr_y);

        int counter_hit = 0;
        int times_counter = 0;

        loop_iterator ptr(scan_result_area);


        // precision 0.1 degree a time
        for (times_counter; times_counter < 3600; times_counter++) {
            double angle = times_counter / 10;
            Line new_line = line.rotate(angle);

            std::vector<double> d_list;
            std::vector<Point> hit_list;
            Point none_hit = { NAN, NAN };

            for (Shape* it : myshapes) {
                if (lidar_range.in_region(it)) {
                    Point hit = (it)->hit(new_line.getter('1'), new_line.getter('2'));
                    if ((!std::isnan(hit.x)) && (!std::isnan(hit.y)) &&
                        lidar_range.point_inside_range(hit.x, hit.y)) {
                        Line temp(curr, hit);
                        d_list.push_back(temp.length());
                        hit_list.push_back(hit);
                    }
                }
                else {
                    continue;
                }
            }

            if (d_list.size() != 0) {
                auto min_it = std::min_element(d_list.begin(), d_list.end());
                auto min_index = std::distance(d_list.begin(), min_it);

                Point each_angle_hit = hit_list[min_index];

                this->scan_result[times_counter] = std::make_pair(each_angle_hit.x, each_angle_hit.y);
                Hit_Angle hit_angle = { times_counter };

                *ptr=hit_angle;
                ++ptr;
                counter_hit++;

            }
            else {
                Point end_point = new_line.getter('2');
                this->scan_result[times_counter] = std::make_pair(end_point.x, end_point.y);

                Hit_Angle hit_angle;

                if (times_counter == 0) {
                    hit_angle.degree = -360;
                }
                else {
                    hit_angle.degree = -times_counter;
                }

                *ptr = hit_angle;
                ++ptr;
            }
        }

        if (counter_hit == 0) {
            this->scan_state = 'w';
        }
        else if (counter_hit == 3600) {
            this->scan_state = 'b';
        }
        else {
            this->scan_state = 'n';
        }
        this->hit_rate = counter_hit/10;

        find_area(max_angle);
        find_nextsteps(type, line,lidar_range);
        
    }

    void find_area(int max_angle) {
        if (scan_state != 'n') {
            return;
        }

        std::vector<Point> area;
        std::vector<int> angles;
        int counter = 0;

        loop_iterator head_ptr(scan_result_area);
        loop_iterator tail_ptr(scan_result_area, false);

        auto ptr = head_ptr;

        if ((*head_ptr).degree < 0) {
            find_next_hit(ptr, tail_ptr);

            auto start_ptr = ptr;
            ++ptr;

            while (true) {
                find_next_not_hit(ptr, start_ptr);

                if (ptr == start_ptr) {
                    break;
                }

                angles.push_back(-(*ptr).degree);

                find_next_hit(ptr, start_ptr);
                auto normal_pre = ptr.prev();
                angles.push_back(-(*normal_pre).degree);

                if (ptr == start_ptr) {
                    break;
                }
            }
        }
        else {
            ++ptr;
            while (true) {
                find_next_not_hit(ptr, tail_ptr);

                if (ptr == tail_ptr) {
                    break;
                }
                angles.push_back(-(*ptr).degree);

                find_next_hit(ptr, tail_ptr);
                auto normal_pre = ptr.prev();
                angles.push_back(-(*normal_pre).degree);

                if (ptr == tail_ptr) {
                    break;
                }
            }
        }

        area_processing(max_angle, angles);
    }

    void area_processing(int max_angle, std::vector<int>& angles) {
        std::vector<int> area_after = angles;
        max_angle = int(max_angle * 10);
        int offset = 0;

        for (int i = 0; i < angles.size(); i += 2) {
            int angle_diff;

            if (angles[i + 1] < angles[i]) {
                angle_diff = std::abs(angles[i + 1] - angles[i] + 3600);
            }
            else {
                angle_diff = std::abs(angles[i + 1] - angles[i]);
            }

            if (angle_diff > max_angle) {
                for (int k = max_angle; k < angle_diff; k += max_angle) {
                    auto it = area_after.begin() + i + 1 + offset;
                    int add = angles[i] + k;

                    if (add >= 3600) {
                        add -= 3600;
                    }
                    area_after.insert(it, add);
                    it = area_after.begin() + i + 1 + offset;
                    area_after.insert(it, add);
                    offset += 2;
                }
            }
        }
        this->angle_list = area_after;
    }

    void find_nextsteps(char type, Line& scan_line, Circle &lidar_range) {
        if (!nextsteps.empty()) {
            this->nextsteps.clear();
        }
        std::vector<std::pair<double, double>> temp_points;

        for (auto it : angle_list) {
            Point end_point = { scan_result[it].first, scan_result[it].second };
            temp_points.push_back(std::make_pair(end_point.x, end_point.y));
        }
        this->area = temp_points;

        if (type == 'm') {

            for (int i = 0; i < temp_points.size(); i += 2) {
                Line temp = { temp_points[i].first, temp_points[i].second,
                             temp_points[i + 1].first, temp_points[i + 1].second };
                Point mid = temp.midpoint();
                this->nextsteps.push_back(std::make_pair(mid.x, mid.y));
            }

        }
        else if (type == 'b') {
            for (int i = 0; i < temp_points.size(); i += 2) {
                Line temp = { temp_points[i].first, temp_points[i].second,
                             temp_points[i + 1].first, temp_points[i + 1].second };
                Point mid = temp.midpoint();
                Point border = lidar_range.project_to_circle(mid.x, mid.y);
                this->nextsteps.push_back(std::make_pair(border.x, border.y));
            }
        }

        else {
            throw std::runtime_error("type error!\n");
        }
    }

    std::vector<std::pair<double, double>> get_result() { return scan_result; }

    bool point_is_nan(Point check) {
        if (std::isnormal(check.x) && std::isnormal(check.y)) {
            return true;
        }
        else {
            return false;
        }
    }

    std::vector<double> get_size() { //for python
        std::vector<double> temp;
        temp.push_back(size[0]);
        temp.push_back(size[1]);

        return temp;
    }

    char get_state() { return scan_state; }

    std::vector<double> get_angles() { 
        std::vector<double> temp;
        for (int it : angle_list) {
            temp.push_back(it / 10);
        }
        return temp; }

    std::vector<std::pair<double, double>> get_nextsteps() { return nextsteps; }
    std::vector<std::pair<double, double>> get_area() { return area; }
    float get_hit_rate() { return hit_rate; }

private:
    std::vector<Shape*> myshapes;
    std::vector<std::string> mynote;
    std::vector<std::pair<double, double>> scan_result;
    std::list<Hit_Angle> scan_result_area;
    std::vector<int> angle_list;
    std::vector<std::pair<double, double>> nextsteps;
    std::vector<std::pair<double, double>> area;

    char scan_state = ' ';
    double size[2] = {0,0};
    int shape_num[2] = {0,0};
    float hit_rate = 0;

    void find_next_not_hit(loop_iterator& ptr, loop_iterator& end) {
        do {
            ++ptr;
            if (ptr == end) {
                break;
            }
        } while (!((*ptr).degree < 0));
    }

    void find_next_hit(loop_iterator& ptr, loop_iterator& end) {
        do {
            ++ptr;
            if (ptr == end) {
                break;
            }
        } while (!((*ptr).degree >= 0));
    }
};

int main() {
    Vector_map vvv;
    vvv.readfile("double_c.txt", "relative");
    vvv.print_out_data();
    vvv.scan(8.0, 9.0, 2, 60, 'm');
    std::vector<double> vec = vvv.get_angles();
    vvv.scan(4.5375908692821, 4.6762052547942, 2, 60, 'm');
    vvv.~Vector_map();
}


namespace py = pybind11;

PYBIND11_MODULE(collis, m) {
	py::class_<Vector_map,std::shared_ptr<Vector_map>>(m, "Vector_map")
		.def(py::init())
		.def("readfile", &Vector_map::readfile)
		.def("create_border", &Vector_map::create_border)
		.def("create_poly", &Vector_map::create_poly)
		.def("create_circle", &Vector_map::create_circle)
        .def(" delete_shape",&Vector_map::delete_shape)
		.def("print_out_data", &Vector_map::print_out_data)
		.def("get_shape_num", &Vector_map::get_shape_num)
		.def("get_shape_list", &Vector_map::get_shape_list, py::return_value_policy::reference)
		.def("scan", &Vector_map::scan)
        .def("scan_one_line",&Vector_map::scan_one_line)
        .def("area_processing", &Vector_map::area_processing)      
		.def("get_result", &Vector_map::get_result)
		.def("get_angles", &Vector_map::get_angles)
        .def("get_area", &Vector_map::get_area)
        .def("get_nextsteps", &Vector_map::get_nextsteps)
        .def("get_size",&Vector_map::get_size)
        .def("get_hit_rate", &Vector_map::get_hit_rate)
		.def("get_state", &Vector_map::get_state);

	py::class_<Point, std::shared_ptr<Point>>(m, "Point")
        .def(py::init<double, double>())
		.def_readonly("x", &Point::x)
		.def_readonly("y", &Point::y);

    py::class_<Eq_Line, std::shared_ptr<Eq_Line>>(m, "Eq_line")
        .def(py::init<double, double,double>())
        .def_readonly("c1", &Eq_Line::c1)
        .def_readonly("c2", &Eq_Line::c2)
        .def_readonly("c3", &Eq_Line::c3);

    py::class_<Line, std::shared_ptr<Line>>(m, "Line")
        .def(py::init<double, double, double, double>())
        .def("print_out", &Line::print_out)
        .def("get_data", &Line::get_data)
        .def("get_v", &Line::get_v)
        .def("find_slope", &Line::find_slope)
        .def("length", &Line::length)
        .def("angle_btw_line", &Line::angle_btw_line)
        .def("dot", &Line::dot_line)
        .def("distance_point2line", &Line::distance_point2line)
        .def("midpoint", &Line::midpoint, py::return_value_policy::reference)
        .def("find_Eq_Line",&Line::find_Eq_Line, py::return_value_policy::reference)
		.def("hit", &Line::hit, py::return_value_policy::reference);

	py::class_<Poly, std::shared_ptr<Poly>>(m, "Poly")
		.def(py::init<std::vector<double>>())
		.def("print_out", &Poly::print_out)
		.def("get_data", &Poly::get_data)
		.def("hit", &Poly::hit, py::return_value_policy::reference);

	py::class_<Circle, std::shared_ptr<Circle>>(m, "Circle")
		.def(py::init<double,double,double>())
		.def("print_out", &Circle::print_out)
		.def("get_data", &Circle::get_data)
        .def("point_inside_range",&Circle::point_inside_range)
        .def("project_to_circle",&Circle::project_to_circle, py::return_value_policy::reference)
        .def("in_region",&Circle::py_inregion)
		.def("hit", &Circle::hit, py::return_value_policy::reference);
        
}
