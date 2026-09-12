#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int kQ = 4;
constexpr int kLength = 8;

using Word = std::array<unsigned char, kLength>;

std::vector<Word> ReadCode(const std::string& path) {
  std::ifstream input(path);
  if (!input) {
    throw std::runtime_error("cannot open code file");
  }
  std::vector<Word> code;
  std::set<std::string> seen;
  std::string line;
  while (std::getline(input, line)) {
    const auto hash = line.find('#');
    if (hash != std::string::npos) {
      line.erase(hash);
    }
    while (!line.empty() &&
           (line.back() == ' ' || line.back() == '\t' || line.back() == '\r')) {
      line.pop_back();
    }
    if (line.empty()) {
      continue;
    }
    if (line.size() != kLength || !seen.insert(line).second) {
      throw std::runtime_error("malformed or duplicate codeword");
    }
    Word word{};
    for (int position = 0; position < kLength; ++position) {
      if (line[position] < '0' || line[position] >= '0' + kQ) {
        throw std::runtime_error("symbol outside quaternary alphabet");
      }
      word[position] =
          static_cast<unsigned char>(line[position] - '0');
    }
    code.push_back(word);
  }
  if (code.empty()) {
    throw std::runtime_error("empty code");
  }
  return code;
}

Word Decode(int value) {
  Word word{};
  for (int position = kLength - 1; position >= 0; --position) {
    word[position] = static_cast<unsigned char>(value % kQ);
    value /= kQ;
  }
  return word;
}

int Distance(const Word& left, const Word& right) {
  int distance = 0;
  for (int position = 0; position < kLength; ++position) {
    distance += left[position] != right[position];
  }
  return distance;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "usage: verify_direct CODE SIZE RADIUS HOLES\n";
    return 2;
  }
  try {
    const auto code = ReadCode(argv[1]);
    const int expected_size = std::stoi(argv[2]);
    const int expected_radius = std::stoi(argv[3]);
    const int expected_holes = std::stoi(argv[4]);
    if (static_cast<int>(code.size()) != expected_size) {
      throw std::runtime_error("unexpected code size");
    }

    std::array<int, kLength + 1> histogram{};
    int radius = 0;
    int holes = 0;
    int total = 1;
    for (int i = 0; i < kLength; ++i) {
      total *= kQ;
    }
    for (int value = 0; value < total; ++value) {
      const Word point = Decode(value);
      int nearest = kLength + 1;
      for (const Word& center : code) {
        const int distance = Distance(point, center);
        if (distance < nearest) {
          nearest = distance;
        }
      }
      ++histogram[nearest];
      if (nearest > radius) {
        radius = nearest;
      }
      if (nearest > 4) {
        ++holes;
      }
    }

    std::cout << "code_size=" << code.size() << '\n';
    std::cout << "exact_covering_radius=" << radius << '\n';
    std::cout << "hole_count=" << holes << '\n';
    for (int distance = 0; distance <= kLength; ++distance) {
      if (histogram[distance] != 0) {
        std::cout << "distance_" << distance << '='
                  << histogram[distance] << '\n';
      }
    }
    if (radius != expected_radius || holes != expected_holes) {
      std::cerr << "result does not match expected radius and hole count\n";
      return 1;
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error=" << error.what() << '\n';
    return 2;
  }
}
