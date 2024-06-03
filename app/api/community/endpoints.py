# app/api/community/router.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.community.models import (
    CommunityQuestion,
    CommunitySolution,
    CreateCommunityQuestion,
)
from app.api.users.models import User
from app.db import db
from bson import ObjectId
from app.dependencies import AuthRole, get_current_user

router = APIRouter()


@router.post("/ask", summary="Ask a question in the community")
async def ask_question(
    question: CreateCommunityQuestion, user: User = Depends(get_current_user)
):
    try:
        new_question_data = question.dict()
        new_question_data["user_id"] = str(user["_id"])
        print(new_question_data["user_id"])
        new_question = CommunityQuestion(**new_question_data)
        db.community_questions.insert_one(new_question.dict())
        return {"message": "Question posted successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while posting the question.",
        )


@router.post("/respond", summary="Respond to a question in the community")
async def respond_question(
    solution: CommunitySolution, user: User = Depends(get_current_user)
):
    try:
        new_solution = solution.dict()
        new_solution["user_id"] = str(user["_id"])
        db.community_solutions.insert_one(new_solution)
        return {"message": "Solution posted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while posting the solution.",
        )


@router.get("/questions", summary="Get community questions with user data")
async def get_questions():
    try:
        questions_cursor = db.community_questions.find().limit(15)
        questions = list(questions_cursor)

        formatted_questions = []

        for question in questions:
            user_id = question.get("user_id")
            user = db.users.find_one({"_id": ObjectId(user_id)})

            if user:
                formatted_question = {
                    "id": str(question["_id"]),
                    "title": question["title"],
                    "description": question["description"],
                    "solutions": question["solutions"],
                    # "createdAt": question["createdAt"],
                    "user": {
                        "id": str(user["_id"]),
                        "name": user["name"],
                        "profile": user["profile"],
                    }
                }
                formatted_questions.append(formatted_question)

        return formatted_questions

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving questions.",
        )


@router.get("/questions/{question_id}", summary="Get a question by ID")
async def get_question(question_id: str):
    try:
        print(question_id)
        question = db.community_questions.find_one({"_id": ObjectId(question_id)})
        user_id = question.get("user_id")
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if question:
            print(question)
            question["_id"] = str(question["_id"]) 
            return {
                "id": str(question["_id"]),
                "title": question["title"],
                "description": question["description"],
                "solutions": question["solutions"],
                "user": {
                    "id": str(user["_id"]),
                    "name": user["name"],
                    "profile": user["profile"],
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
    except Exception as e:
        print(e)
        print("Error getting the question")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the question.",
        )


@router.put("/{question_id}", summary="Edit a question by ID")
async def edit_question(
    question_id: str,
    updated_question: CommunityQuestion,
    user: User = Depends(get_current_user),
):
    try:
        existing_question = db.community_questions.find_one(
            {"_id": ObjectId(question_id)}
        )
        if existing_question:
            if str(existing_question["user_id"]) == str(user["_id"]):
                updated_question_data = updated_question.dict(exclude_unset=True)
                db.community_questions.update_one(
                    {"_id": ObjectId(question_id)}, {"$set": updated_question_data}
                )
                return {"message": "Question updated successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not authorized to edit this question.",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the question.",
        )


@router.delete("/{question_id}", summary="Delete a question by ID")
async def delete_question(question_id: str, user: User = Depends(get_current_user)):
    try:
        existing_question = db.community_questions.find_one(
            {"_id": ObjectId(question_id)}
        )
        if existing_question:
            if str(existing_question["user_id"]) == str(user["_id"]):
                db.community_questions.delete_one({"_id": ObjectId(question_id)})
                return {"message": "Question deleted successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not authorized to delete this question.",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the question.",
        )


@router.put("/respond/{solution_id}", summary="Edit a solution by ID")
async def edit_solution(
    solution_id: str,
    updated_solution: CommunitySolution,
    user: User = Depends(get_current_user),
):
    try:
        existing_solution = db.community_solutions.find_one(
            {"_id": ObjectId(solution_id)}
        )
        if existing_solution:
            if str(existing_solution["user_id"]) == str(user["_id"]):
                updated_solution_data = updated_solution.dict(exclude_unset=True)
                db.community_solutions.update_one(
                    {"_id": ObjectId(solution_id)}, {"$set": updated_solution_data}
                )
                return {"message": "Solution updated successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not authorized to edit this solution.",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Solution not found"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the solution.",
        )


@router.delete("/respond/{solution_id}", summary="Delete a solution by ID")
async def delete_solution(solution_id: str, user: User = Depends(get_current_user)):
    try:
        existing_solution = db.community_solutions.find_one(
            {"_id": ObjectId(solution_id)}
        )
        if existing_solution:
            if str(existing_solution["user_id"]) == str(user["_id"]):
                db.community_solutions.delete_one({"_id": ObjectId(solution_id)})
                return {"message": "Solution deleted successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not authorized to delete this solution.",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Solution not found"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the solution.",
        )
