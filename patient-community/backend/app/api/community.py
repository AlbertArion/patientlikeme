from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from ..database import get_db
from ..models.user import User
from ..models.community import Community, Post, Comment
from ..utils.security import get_current_user

router = APIRouter(tags=["社区"])

class CommunityResponse(BaseModel):
    id: int
    name: str
    description: str
    member_count: int
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    community_id: int
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    user_id: int
    community_id: int
    title: str
    content: str
    likes_count: int
    comments_count: int
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

@router.get("/communities", response_model=List[CommunityResponse])
def get_communities(db: Session = Depends(get_db)):
    """获取社区列表"""
    communities = db.query(Community).all()
    return communities

@router.get("/communities/{community_id}/posts", response_model=List[PostResponse])
def get_community_posts(
    community_id: int,
    db: Session = Depends(get_db)
):
    """获取社区帖子"""
    posts = db.query(Post).filter(
        Post.community_id == community_id
    ).order_by(Post.created_at.desc()).all()
    
    return posts

@router.post("/posts", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发布帖子"""
    post = Post(
        user_id=current_user.id,
        community_id=post_data.community_id,
        title=post_data.title,
        content=post_data.content
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

@router.post("/posts/{post_id}/comments")
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发表评论"""
    # 检查帖子是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    
    db.add(comment)
    
    # 更新评论数
    post.comments_count += 1
    
    db.commit()
    
    return {"message": "评论成功"}

@router.post("/posts/{post_id}/like")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """点赞帖子"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )
    
    post.likes_count += 1
    db.commit()
    
    return {"message": "点赞成功"}
