# terraform/main.tf

provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_instance" "lunch_bot_server" {
  ami           = "ami-0c9c942bd7bf113a2"
  instance_type = "t3.small"
  vpc_security_group_ids = [aws_security_group.lunch_bot_sg.id]
  key_name      = "lunch-bot-key" 

  tags = {
    Name = "iloveawschoolunch-server"
  }
}

resource "aws_security_group" "lunch_bot_sg" {
  name        = "lunch-bot-sg"
  description = "Security Group for Lunch Bot server"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

    ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "iloveawschoolunch-sg"
  }
}


# 5. S3 버킷(Frontend 저장소) 정의
resource "aws_s3_bucket" "lunch_bot_frontend_bucket" {
  # bucket 이름이 lunch_bot_frontend_bucket으로 통일되었습니다.
  bucket = "iloveawschoolunch-frontend-bucket-${random_id.bucket_suffix.hex}"
}

# 6. S3 버킷 이름에 붙일 랜덤 문자열 생성
resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket_public_access_block" "lunch_bot_frontend_bucket_access" { 
  bucket = aws_s3_bucket.lunch_bot_frontend_bucket.id

  block_public_acls     = false
  block_public_policy   = false
  ignore_public_acls    = false
  restrict_public_buckets = false
}

# 7. S3 버킷을 웹사이트처럼 접근 가능하게 설정
resource "aws_s3_bucket_website_configuration" "lunch_bot_frontend_bucket_config" {
  bucket = aws_s3_bucket.lunch_bot_frontend_bucket.id
  index_document {
    suffix = "index.html"
  }
}

# 8. S3 버킷을 전 세계에 공개(Public) 설정
resource "aws_s3_bucket_policy" "lunch_bot_frontend_bucket_policy" {
  bucket = aws_s3_bucket.lunch_bot_frontend_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.lunch_bot_frontend_bucket.arn}/*"
      }
    ]
  })
  depends_on = [aws_s3_bucket_public_access_block.lunch_bot_frontend_bucket_access]
}

resource "aws_eip" "lunch_bot_eip" {
  domain = "vpc"

  tags = {
    Name = "iloveawschoolunch-eip"
  }
}

resource "aws_eip_association" "eip_assoc" {
  instance_id = aws_instance.lunch_bot_server.id
  allocation_id = aws_eip.lunch_bot_eip.id
}