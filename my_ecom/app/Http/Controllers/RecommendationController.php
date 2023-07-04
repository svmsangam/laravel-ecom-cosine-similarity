<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class RecommendationController extends Controller
{
    public function getRecommendations(Request $request)
    {
        $productId = $request->input('product_id'); // Input product ID for which you want recommendations

        // Retrieve the product's category and color
        $product = DB::table('products')
            ->join('products_attr', 'products.id', '=', 'products_attr.products_id')
            ->join('categories', 'products.category_id', '=', 'categories.id')
            ->join('colors', 'products_attr.color_id', '=', 'colors.id')
            ->select('categories.category_name as category', 'colors.color as color')
            ->where('products.id', $productId)
            ->first();

        // Retrieve recommendations based on the product's category and color
        $recommendations = DB::table('products')
            ->join('products_attr', 'products.id', '=', 'products_attr.products_id')
            ->join('categories', 'products.category_id', '=', 'categories.id')
            ->join('colors', 'products_attr.color_id', '=', 'colors.id')
            ->select('products.id', 'products.name')
            ->where('categories.category_name', $product->category)
            ->where('colors.color', $product->color)
            ->where('products.id', '!=', $productId)
            ->limit(5) // Limit the number of recommendations
            ->get();

        return response()->json($recommendations);
    }
}
